import chainlit as cl

# 1. Handler de Início: Dispara quando o usuário abre o chat
@cl.on_chat_start
async def start():
    # Aqui você pode definir uma mensagem de boas-vindas personalizada
    await cl.Message(content="Olá! Eu sou o seu assistente virtual. Como posso te ajudar hoje?").send()

# 2. Handler de Mensagem: Dispara cada vez que o usuário envia um texto
@cl.on_message
async def main(message: cl.Message):
    # Aqui é onde a mágica acontece. Por enquanto, vamos fazer um "Eco"
    # Depois, conectaremos a lógica da IA aqui.
    
    resposta = f"Você disse: {message.content}"
    
    await cl.Message(content=resposta).send()