from langchain.chat_models import BaseChatModel, init_chat_model


def load_llm() -> BaseChatModel:
    return init_chat_model("google_genai:gemini-2.5-flash")


# return init_chat_model("ollama:gpt-oss:20b")
# return init_chat_model("openai:gpt-4o-mini", temperature=0.5)
# return init_chat_model("ollama:llama3.2")
