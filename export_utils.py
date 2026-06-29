import os
from datetime import datetime


def clean_filename(text):
    allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_ "
    cleaned = "".join(char for char in text if char in allowed_chars)
    cleaned = cleaned.strip().replace(" ", "_")
    return cleaned[:50] if cleaned else "conversation"


def export_conversation_to_txt(conversation_id, title, messages):
    os.makedirs("exports", exist_ok=True)

    safe_title = clean_filename(title or f"conversation_{conversation_id}")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_name = f"conversation_{conversation_id}_{safe_title}_{timestamp}.txt"
    file_path = os.path.join("exports", file_name)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(f"Conversation ID: {conversation_id}\n")
        file.write(f"Title: {title}\n")
        file.write(f"Exported At: {datetime.now()}\n")
        file.write("=" * 60)
        file.write("\n\n")

        for message_id, sender, message, created_at in messages:
            role = "User" if sender == "user" else "Assistant"

            file.write(f"{role} ({created_at})\n")
            file.write("-" * 60)
            file.write("\n")
            file.write(message)
            file.write("\n\n")

    return file_path