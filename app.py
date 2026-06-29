import os
from export_utils import export_conversation_to_txt

import chainlit as cl

@cl.password_auth_callback
def auth_callback(username: str, password: str):
    if password == "demo123":
        return cl.User(
            identifier=username,
            metadata={"role": "user"}
        )
    return None

from databricks_client import call_databricks_rag
from database import (
    initialize_database,
    get_or_create_user,
    create_conversation,
    save_message,
    update_conversation_title,
    get_conversations_by_user,
    get_messages_by_conversation,
    get_conversation_title,
    save_feedback,
)


CURRENT_USERNAME = "varun"
CURRENT_DISPLAY_NAME = "Varun"


@cl.on_chat_start
async def start():
    initialize_database()

    user = cl.user_session.get("user")
    username = user.identifier

    user_id = get_or_create_user(username, username)
    conversation_id = create_conversation(user_id, "New conversation")

    cl.user_session.set("user_id", user_id)
    cl.user_session.set("conversation_id", conversation_id)

    conversations = get_conversations_by_user(user_id)

    actions = [
        cl.Action(name="new_chat", payload={"conversation_id": conversation_id}, label="New Chat"),
        cl.Action(name="export_conversation", payload={}, label="Export Current Conversation"),
    ]

    for convo in conversations[:5]:
        old_conversation_id, title, created_at, last_updated, message_count = convo
        actions.append(
            cl.Action(
                name="load_conversation",
                payload={"conversation_id": old_conversation_id},
                label=f"{title} ({message_count} msgs)"
            )
        )

    await cl.Message(
        content="Select a previous conversation or start a new chat:",
        actions=actions
    ).send()

    await cl.Message(
        content="Hello! I am connected to your Databricks RAG agent. Ask me a question."
    ).send()


@cl.on_message
async def main(message: cl.Message):
    conversation_id = cl.user_session.get("conversation_id")
    user_question = message.content

    

    save_message(conversation_id, "user", user_question)

    message_count = cl.user_session.get("message_count") or 0

    if message_count == 0:
        title = user_question[:50]
        update_conversation_title(conversation_id, title)

    cl.user_session.set("message_count", message_count + 1)

    msg = cl.Message(content="Thinking...")
    await msg.send()

    answer = call_databricks_rag(user_question)

    assistant_message_id = save_message(conversation_id, "assistant", answer)

    msg.content = answer
    msg.actions = [
        cl.Action(
            name="feedback_positive",
            payload={"message_id": assistant_message_id},
            label="Helpful"
        ),
        cl.Action(
            name="feedback_negative",
            payload={"message_id": assistant_message_id},
            label="Not Helpful"
        ),
    ]

    await msg.update()

@cl.action_callback("new_chat")
async def on_new_chat(action: cl.Action):
    await cl.Message(content="New chat is ready. Ask your question.").send()


@cl.action_callback("load_conversation")
async def on_load_conversation(action: cl.Action):
    conversation_id = action.payload["conversation_id"]
    cl.user_session.set("conversation_id", conversation_id)

    messages = get_messages_by_conversation(conversation_id)

    await cl.Message(content="Loaded previous conversation:").send()

    for message_id, sender, text, created_at in messages:
        role = "You" if sender == "user" else "Assistant"
        await cl.Message(content=f"**{role}:** {text}").send()


@cl.action_callback("feedback_positive")
async def on_feedback_positive(action: cl.Action):
    message_id = action.payload["message_id"]
    save_feedback(message_id, 1, "Helpful")

    await cl.Message(
        content="Thanks for your feedback. Marked as helpful."
    ).send()


@cl.action_callback("feedback_negative")
async def on_feedback_negative(action: cl.Action):
    message_id = action.payload["message_id"]
    save_feedback(message_id, -1, "Not helpful")

    await cl.Message(
        content="Thanks for your feedback. Marked as not helpful."
    ).send()


@cl.action_callback("export_conversation")
async def on_export_conversation(action: cl.Action):
    conversation_id = cl.user_session.get("conversation_id")

    if not conversation_id:
        await cl.Message(content="No active conversation found to export.").send()
        return

    title = get_conversation_title(conversation_id)
    messages = get_messages_by_conversation(conversation_id)

    if not messages:
        await cl.Message(content="No messages found in this conversation yet.").send()
        return

    file_path = export_conversation_to_txt(conversation_id, title, messages)
    file_name = os.path.basename(file_path)

    with open(file_path, "rb") as file:
        file_content = file.read()

    await cl.Message(
        content="Your conversation export is ready. Download the file below.",
        elements=[
            cl.File(
                name=file_name,
                content=file_content,
                mime="text/plain",
            )
        ],
    ).send()