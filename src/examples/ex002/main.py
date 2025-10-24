from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from rich import print

# Load environment variables from .env file
load_dotenv()

llm = init_chat_model(
    "gemini-2.5-flash", model_provider="google_genai", temperature=0.7
)

# Persona AI
system_message = SystemMessage("""Você é Professor Aurelius, um renomado historiador, contador de histórias e guardião da memória humana.
Seu papel é criar e narrar histórias de forma envolvente, educativa e emocionante.
Você respeita o tempo, a cultura e as emoções das pessoas.
Sua fala é gentil, articulada, curiosa e profundamente empática.

Tom de voz: acolhedor, sábio, inspirador, narrativo e vívido.

Objetivo Principal:
Criar histórias originais e cativantes com base no tema solicitado pelo usuário.
Cada história deve despertar imaginação, moral e emoção.
Sua especialidade e historias sobre a segunda guerra mundial, com fatos reais.

insira emoji para deixa a conversa mais atrativa""")  # noqa: E501

# Input do Humano
human_message = HumanMessage("Ola, meu nome e Andrey")

# Voce pode enviar uma lista de mensagens para o modelo com o historico de-
# conversas. Se nao fizer isso, cada mensagem sera tratada como a primeira
# mensagem recebida pelo modelo, ele nao sabera nada sobre as conversas
# anteriores.
messages = [system_message, human_message]
response = llm.invoke(messages)
print(f"{'AI':-^80}")
print(response.content)  # Em response.content, teremos uma AIMessage neste contexto
# Tambem podemos fazer um loop infinito e montar um historico de conversa
# artificialmente. Mas isso nao e necessario quando usamos o LangGraph

# Adiciona a resposta do modelo em messages - Iniciando o Loop
messages.append(response)
while True:
    # Pega a mensagem do usuario
    print(f"{'Human':-^80}")
    user_input = input("Digite sua mensagem:")
    human_message = HumanMessage(user_input)

    # qualquer uma dessas palavras termina o loop
    if user_input.lower() in ["exit", "quit", "bye", "q"]:
        break

    # Adiciona a mensagem do usuario
    messages.append(human_message)

    # Manda as mensagens com o historico de volta para o modelo
    response = llm.invoke(messages)

    # Exibe a mensagem do modelo
    print(f"{'AI':-^80}")
    print(response.content)
    print()

    # Adiciona a resposta do modelo em messages
    messages.append(response)

    # Isso e so para vermos como ficou nosso historico de conversas
    print()
    print(f"{'Historico':-^80}")
    print(*[f"{m.type.upper()}\n{m.content}\n\n" for m in messages], sep="", end="")
    print()
