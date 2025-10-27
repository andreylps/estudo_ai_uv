import operator
from typing import Annotated, TypedDict
from urllib import response

from langgraph.graph import StateGraph
from rich import print

# def reducer(a: list[str], b: list[str]) -> list[str]:
#  #  return a + b


# 1 - Definir o meu Estado
class State(TypedDict):
    nodes_path: Annotated[list[str], operator.add]


# 2 - Definindo o nodes
def node_a(state: State) -> State:
    output_state: State = {"nodes_path": ["A"]}
    print("> node_a", f"{state=}", f"{output_state=}")
    return output_state


def node_b(state: State) -> State:
    output_state: State = {"nodes_path": ["B"]}
    print("> node_b", f"{state=}", f"{output_state=}")
    return output_state


# Definir o build do grafo
builder = StateGraph(State)

builder.add_node("A", node_a)
builder.add_node("B", node_b)

builder.add_edge("__start__", "A")
builder.add_edge("A", "B")
builder.add_edge("B", "__end__")

# Complilar o Grafo
graph = builder.compile()

# Pegar o Resultado
response = graph.invoke({"nodes_path": []})  # noqa: F811

# Resultado de todo o grafo
print()
print(f"{response=}")
print()
