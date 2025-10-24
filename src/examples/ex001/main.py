from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from rich import print

# Load environment variables from .env file
load_dotenv()

llm = init_chat_model("gpt-4o-mini", model_provider="openai", temperature=0.7)

response = llm.invoke("Ola seja bem vindo!")

print(response)
