import threading
from collections.abc import Sequence
from logging import config
from typing import Annotated, TypedDict

from langchain.chat_models import init_chat_model
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph, add_messages
from langgraph.graph.state import RunnableConfig
from rich import print
from rich.markdown import Markdown

# 0 - Chamando a LLM
llm = init_chat_model("google_genai:gemini-2.5-flash")
# llm = init_chat_model("openai:gpt-4o-mini")


# 1 - Defino meu state
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


# 2 - Defino meus nodes
def call_llm(state: AgentState) -> AgentState:
    llm_result = llm.invoke(state["messages"])
    return {"messages": [llm_result]}


# 3 - Crio o StateGraph
builder = StateGraph(
    AgentState, context_schema=None, input_schema=AgentState, output_schema=AgentState
)

# 4 Adicionar nodes no Grafo
builder.add_node("call_llm", call_llm)
builder.add_edge(START, "call_llm")
builder.add_edge("call_llm", END)

# 5 Compilar o Grafo
checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)
config = RunnableConfig(configurable={"thread_id": threading.get_ident()})  # noqa: F811
if __name__ == "__main__":
    # 6 - Usar o Grafo
    while True:
        use_input = input("Digite sua mensagem:")
        print(Markdown("---"))

        if use_input.lower() in ["q", "quit", "exit"]:
            print("Bye 👋")
            print(Markdown("---"))
            break

        human_message = HumanMessage(use_input)
        result = graph.invoke({"messages": [human_message]}, config=config)

        print(Markdown(str(result["messages"][-1].content)))
        print(Markdown("---"))
