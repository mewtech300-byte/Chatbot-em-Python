## Dia 07. Etapa final da finalização do código e do projeto:
# Projeto Final - 7 Days Of Code (IA e Chainlit)

Este é o projeto de finalização do desafio, onde desenvolvemos um chatbot inteligente utilizando **Chainlit**, **LangChain** e modelos da **Hugging Face**.

##  Como rodar o projeto

###  Instalação das dependências
No ambiente do Colab ou terminal, instale as bibliotecas necessárias:
```bash
pip install chainlit pyngrok langchain optimum auto-gptq --extra-index-url [https://huggingface.github.io/autogptq-index/whl/cu118/](https://huggingface.github.io/autogptq-index/whl/cu118/)

### Configuração do Túnel (Ngrok)
from pyngrok import ngrok
!ngrok config add-authtoken "SEU_TOKEN_AQUI"
print(ngrok.connect(8000).public_url)

### Código de Aplicação (app.py)
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain.llms import HuggingFacePipeline
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
import chainlit as cl

# Configuração do Modelo Zephyr
model_name_or_path = "TheBloke/zephyr-7B-beta-GPTQ"
tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)
model = AutoModelForCausalLM.from_pretrained(model_name_or_path, device_map="auto")

pipe = pipeline(
    task="text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=512
)

llm = HuggingFacePipeline(pipeline=pipe)

template = """
You are a helpful assistant that provides information and engages in casual conversation.
Respond naturally to user queries and provide useful information.
Please, write a single reply only!

Current conversation:
{history}
Question: {input}
"""

prompt = PromptTemplate(input_variables=["history", "input"], template=template)
memory = ConversationBufferWindowMemory(k=3)

@cl.on_chat_start
async def start():
    llm_chain = ConversationChain(prompt=prompt, llm=llm, memory=memory)
    cl.user_session.set("llm_chain", llm_chain)

@cl.on_message
async def main(message: cl.message):
    llm_chain = cl.user_session.get("llm_chain")
    cb = cl.AsyncLangchainCallbackHandler()
    cb.answer_reached = True

    res = await cl.make_async(llm_chain)(message.content, callbacks=[cb])
    response_text = res['response'].split("Answer:")[-1].strip()

    await cl.Message(content=response_text).send()

### Para iniciarmos o servidor do chat:
chainlit run app.py
