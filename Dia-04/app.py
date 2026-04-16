import chainlit as cl
from transformers import pipeline

# 1. Inicialização do Modelo e Tokenizador (via Pipeline)
# O GPT-2 é leve e perfeito para esse teste inicial
print("Iniciando o motor do Chatbot...")
pipe = pipeline("text-generation", model="gpt2")

@cl.on_chat_start
async def start():
    cl.user_session.set("pipeline", pipe)
    await cl.Message(content="Olá! O Chatbot  está online. Como posso ajudar?").send()

@cl.on_message
async def main(message: cl.Message):
    # 2. Configuração da pipeline de processamento
    pipe = cl.user_session.get("pipeline")
    
    # Gerando a resposta
    prompt = f"Usuário: {message.content}\nIA:"
    raw_res = pipe(prompt, max_new_tokens=50, truncation=True)
    res = raw_res[0]['generated_text'].split("IA:")[-1].strip()
    
    # 3. Enviando a resposta para a interface
    await cl.Message(content=res).send()
