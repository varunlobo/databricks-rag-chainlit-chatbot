import chainlit as cl

from databricks_client import call_databricks_rag
from database import (
    initialize_database,
    get_or_create_user,
    create_conversation,
    save_message,
)


CURRENT_USERNAME = "varun"
CURRENT_DISPLAY_NAME = "Varun"


@cl.on_chat_start
async def start():
    initialize_database()

    user_id = get_or_create_user(CURRENT_USERNAME, CURRENT_DISPLAY_NAME)
    conversation_id = create_conversation(user_id, "New conversation")

    cl.user_session.set("user_id", user_id)
    cl.user_session.set("conversation_id", conversation_id)

    await cl.Message(
        content="Hello! I am connected to your Databricks RAG agent. Ask me a question."
    ).send()


@cl.on_message
async def main(message: cl.Message):
    conversation_id = cl.user_session.get("conversation_id")
    user_question = message.content

    save_message(conversation_id, "user", user_question)

    msg = cl.Message(content="Thinking...")
    await msg.send()

    answer = call_databricks_rag(user_question)

    save_message(conversation_id, "assistant", answer)

    msg.content = answer
    await msg.update()