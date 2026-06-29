# Project Architecture

## Databricks RAG Chainlit Chatbot

This project uses Chainlit as the chatbot interface and connects to a Databricks Model Serving endpoint that hosts a RAG agent. SQLite is used to store users, conversations, messages, and feedback.

## High-Level Architecture

```mermaid
flowchart TD
    A[User] --> B[Chainlit Chat UI]

    B --> C[Python Application app.py]

    C --> D[Databricks Client]
    D --> E[Databricks Model Serving Endpoint]
    E --> F[RAG Agent Response]

    C --> G[SQLite Database]

    G --> H[Users Table]
    G --> I[Conversations Table]
    G --> J[Messages Table]
    G --> K[Feedback Table]

    C --> L[Export Utility]
    L --> M[TXT Conversation Export]
```

## Application Flow

```mermaid
sequenceDiagram
    participant User
    participant Chainlit
    participant App
    participant SQLite
    participant Databricks

    User->>Chainlit: Login
    Chainlit->>App: Start chat session
    App->>SQLite: Create or retrieve user
    App->>SQLite: Create conversation

    User->>Chainlit: Send message
    Chainlit->>App: Pass user message
    App->>SQLite: Save user message
    App->>Databricks: Send message to RAG endpoint
    Databricks-->>App: Return RAG response
    App->>SQLite: Save assistant response
    App-->>Chainlit: Display response
    Chainlit-->>User: Show answer

    User->>Chainlit: Click Helpful / Not Helpful
    App->>SQLite: Save feedback

    User->>Chainlit: Export conversation
    App->>SQLite: Retrieve conversation messages
    App->>App: Generate TXT file
    Chainlit-->>User: Download export
```

## Main Components

| Component              | Purpose                                             |
| ---------------------- | --------------------------------------------------- |
| Chainlit UI            | Provides the web-based chatbot interface            |
| app.py                 | Main application logic and Chainlit event handlers  |
| databricks_client.py   | Sends user questions to the Databricks endpoint     |
| SQLite database        | Stores users, conversations, messages, and feedback |
| database/repository.py | Contains database helper functions                  |
| export_utils.py        | Generates downloadable conversation export files    |
| .chainlit/config.toml  | Stores Chainlit UI branding and configuration       |

## Database Relationship

```mermaid
erDiagram
    USERS ||--o{ CONVERSATIONS : owns
    CONVERSATIONS ||--o{ MESSAGES : contains
    MESSAGES ||--o{ FEEDBACK : receives

    USERS {
        int user_id
        string username
        string display_name
        datetime created_at
    }

    CONVERSATIONS {
        int conversation_id
        int user_id
        string title
        datetime created_at
        datetime last_updated
    }

    MESSAGES {
        int message_id
        int conversation_id
        string sender
        string message
        datetime created_at
    }

    FEEDBACK {
        int feedback_id
        int message_id
        int rating
        string comment
        datetime created_at
    }
```

## Future Production Authentication

The current project uses simple Chainlit password authentication for demonstration.

In a production environment, this can be replaced with Azure Active Directory or enterprise SSO. The authenticated user identity can then be mapped to the existing SQLite user table or a production database.
