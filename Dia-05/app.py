import chainlit as cl
from transformers import pipeline

# Inicializamos a pipeline de geração de texto
generator = pipeline("text-generation", model="gpt2")

@cl.on_chat_start
async def start():
    # Inicializamos a memória vazia no início da conversa
    cl.user_session.set("history", "")
    await cl.Message(content="Olá! Eu sou o seu Chatbot com memória. Como posso ajudar hoje?").send()

@cl.on_message
async def main(message: cl.Message):
    # 1. Recuperamos o que foi dito antes
    history = cl.user_session.get("history")
    
    # 2. Definimos as instruções do sistema (Prompt Engineering)
    system_instruction = "You are a helpful assistant. Answer simply, short and naturally."
    
    # 3. Montamos o prompt completo (Instrução + Histórico + Nova Mensagem)
    full_prompt = f"{system_instruction}\n{history}\nUser: {message.content}\nAssistant:"
    
    # 4. O modelo gera a resposta baseada em todo o contexto
    response = generator(full_prompt, max_new_tokens=30, do_sample=True, temperature=0.7, pad_token_id=50256)
    
    # Limpamos a resposta para pegar apenas o que o Assistente disse agora
    generated_text = response[0]["generated_text"]
    answer = generated_text.split("Assistant:")[-1].split("User:")[0].strip()
    
    # 5. Atualizamos a memória para a próxima pergunta
    new_history = f"{history}\nUser: {message.content}\nAssistant: {answer}"
    cl.user_session.set("history", new_history)

    await cl.Message(content=answer).send()
