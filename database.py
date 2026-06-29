import sqlite3

DB_NAME = "chat_history.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            display_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            conversation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            message_id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER NOT NULL,
            sender TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(conversation_id) REFERENCES conversations(conversation_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id INTEGER NOT NULL,
            rating INTEGER,
            comment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(message_id) REFERENCES messages(message_id)
        )
    """)

    conn.commit()
    conn.close()

def get_or_create_user(username, display_name=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT user_id FROM users WHERE username = ?",
        (username,)
    )
    row = cursor.fetchone()

    if row:
        conn.close()
        return row[0]

    cursor.execute(
        "INSERT INTO users (username, display_name) VALUES (?, ?)",
        (username, display_name or username)
    )

    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id


def create_conversation(user_id, title):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO conversations (user_id, title) VALUES (?, ?)",
        (user_id, title)
    )

    conn.commit()
    conversation_id = cursor.lastrowid
    conn.close()
    return conversation_id


def save_message(conversation_id, sender, message):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO messages (conversation_id, sender, message)
        VALUES (?, ?, ?)
        """,
        (conversation_id, sender, message)
    )

    cursor.execute(
        """
        UPDATE conversations
        SET last_updated = CURRENT_TIMESTAMP
        WHERE conversation_id = ?
        """,
        (conversation_id,)
    )

    conn.commit()
    message_id = cursor.lastrowid
    conn.close()
    return message_id



if __name__ == "__main__":
    initialize_database()

    user_id = get_or_create_user("varun", "Varun")
    conversation_id = create_conversation(user_id, "Test conversation")
    save_message(conversation_id, "user", "Hello")
    save_message(conversation_id, "assistant", "Hello! How can I assist you today?")

    print("Database test completed successfully.")
    print("User ID:", user_id)
    print("Conversation ID:", conversation_id)