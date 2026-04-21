## Dia 07. Etapa final da finalização do código e do projeto:
{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": []
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "N2GfBtIKbilg"
      },
      "outputs": [],
      "source": [
        "# Atenção: se você quiser rodar mais de uma vez as células, esta aqui só é necessária uma vez no mesmo ambiente de execução\n",
        "!pip3 install chainlit pyngrok langchain optimum auto-gptq --extra-index-url https://huggingface.github.io/autogptq-index/whl/cu118/ -q"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!ngrok config add-authtoken \"seu-token-aqui\""
      ],
      "metadata": {
        "id": "UVYQ8MlMd-ul"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "from pyngrok import ngrok\n",
        "print(ngrok.connect(8000).public_url)"
      ],
      "metadata": {
        "id": "G9iG3xfZfBqj"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "%%writefile app.py\n",
        "from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline\n",
        "from langchain.llms import HuggingFacePipeline\n",
        "from langchain.prompts.prompt import PromptTemplate\n",
        "from langchain.chains import ConversationChain\n",
        "from langchain.memory import ConversationBufferWindowMemory\n",
        "import chainlit as cl\n",
        "\n",
        "model_name_or_path = \"TheBloke/zephyr-7B-beta-GPTQ\"\n",
        "tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)\n",
        "model = AutoModelForCausalLM.from_pretrained(model_name_or_path, device_map=\"auto\")\n",
        "\n",
        "pipe = pipeline(\n",
        "    task=\"text-generation\",\n",
        "    model=model,\n",
        "    tokenizer=tokenizer,\n",
        "    max_new_tokens=512\n",
        "    )\n",
        "\n",
        "llm=HuggingFacePipeline(pipeline=pipe)\n",
        "\n",
        "template = \"\"\"\n",
        "\n",
        "You are a helpful assistant that provides information and engages in casual conversation.\n",
        "Respond naturally to user queries and provide useful information.\n",
        "Please, write a single reply only!\n",
        "</s>\n",
        "\n",
        "Current conversation:\n",
        "{history}\n",
        "Question: {input}\n",
        "</s>\n",
        "\n",
        "\"\"\"\n",
        "\n",
        "prompt = PromptTemplate(input_variables=[\"history\", \"input\"], template=template)\n",
        "memory=ConversationBufferWindowMemory(k=3)\n",
        "\n",
        "@cl.on_chat_start\n",
        "async def start():\n",
        "    llm_chain = ConversationChain(prompt=prompt, llm=llm, memory=memory)\n",
        "    cl.user_session.set(\"llm_chain\", llm_chain)\n",
        "\n",
        "@cl.on_message\n",
        "async def main(message: cl.message):\n",
        "    llm_chain = cl.user_session.get(\"llm_chain\")\n",
        "    cb = cl.AsyncLangchainCallbackHandler()\n",
        "    cb.answer_reached = True\n",
        "\n",
        "    res = await cl.make_async(llm_chain)(message.content, callbacks=[cb])\n",
        "\n",
        "    response_text = res['response'].split(\"Answer:\")[-1].strip()\n",
        "\n",
        "    await cl.Message(content=response_text).send()"
      ],
      "metadata": {
        "id": "Qwo1uHSafjZt"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "!chainlit run app.py"
      ],
      "metadata": {
        "id": "X8NjqR-ZgjAc"
      },
      "execution_count": null,
      "outputs": []
    }
  ]
}
