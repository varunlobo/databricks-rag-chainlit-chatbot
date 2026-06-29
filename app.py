import chainlit as cl
from databricks_client import call_databricks_rag


@cl.on_chat_start
async def start():
    await cl.Message(
        content="Hello! I am connected to your Databricks RAG agent. Ask me a question."
    ).send()


@cl.on_message
async def main(message: cl.Message):
    user_question = message.content

    msg = cl.Message(content="Thinking...")
    await msg.send()

    answer = call_databricks_rag(user_question)

    msg.content = answer
    await msg.update()