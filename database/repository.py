from database.connection import get_connection


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

    message_id = cursor.lastrowid

    cursor.execute(
        """
        UPDATE conversations
        SET last_updated = CURRENT_TIMESTAMP
        WHERE conversation_id = ?
        """,
        (conversation_id,)
    )

    conn.commit()
    conn.close()
    return message_id

def get_conversations_by_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            c.conversation_id,
            c.title,
            c.created_at,
            c.last_updated,
            COUNT(m.message_id) AS message_count
        FROM conversations c
        LEFT JOIN messages m
            ON c.conversation_id = m.conversation_id
        WHERE c.user_id = ?
        GROUP BY c.conversation_id
        ORDER BY c.last_updated DESC
        """,
        (user_id,)
    )

    conversations = cursor.fetchall()
    conn.close()
    return conversations


def get_messages_by_conversation(conversation_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            message_id,
            sender,
            message,
            created_at
        FROM messages
        WHERE conversation_id = ?
        ORDER BY created_at ASC
        """,
        (conversation_id,)
    )

    messages = cursor.fetchall()
    conn.close()
    return messages

def update_conversation_title(conversation_id, title):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE conversations
        SET title = ?, last_updated = CURRENT_TIMESTAMP
        WHERE conversation_id = ?
        """,
        (title, conversation_id)
    )

    conn.commit()
    conn.close()


def get_latest_conversation_by_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT conversation_id, title, created_at, last_updated
        FROM conversations
        WHERE user_id = ?
        ORDER BY last_updated DESC
        LIMIT 1
        """,
        (user_id,)
    )

    conversation = cursor.fetchone()
    conn.close()
    return conversation

def get_conversation_title(conversation_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT title
        FROM conversations
        WHERE conversation_id = ?
        """,
        (conversation_id,)
    )

    row = cursor.fetchone()
    conn.close()

    return row[0] if row else None

def save_feedback(message_id, rating, comment=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO feedback (message_id, rating, comment)
        VALUES (?, ?, ?)
        """,
        (message_id, rating, comment)
    )

    conn.commit()
    feedback_id = cursor.lastrowid
    conn.close()
    return feedback_id