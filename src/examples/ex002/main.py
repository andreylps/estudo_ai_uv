from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage
from rich import print

# Load environment variables from .env file
load_dotenv()

llm = init_chat_model(
    "gemini-2.5-flash", model_provider="google_genai", temperature=0.7
)
system_message = SystemMessage("Voce e um assisnte de guia de estudo")
response = llm.invoke("Ola seja bem vindo!")
print(response)
