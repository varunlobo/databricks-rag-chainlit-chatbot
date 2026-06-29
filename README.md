# Databricks RAG Chainlit Chatbot

A Python-based chatbot interface built with Chainlit that connects to a Databricks Model Serving endpoint hosting a Retrieval-Augmented Generation (RAG) agent.

The application provides a front-facing chat UI, stores conversation history in SQLite, supports multiple demo users, captures response feedback, and allows users to export conversations.

## Project Objective

The objective of this project is to develop an AI chatbot interface using a purpose-built Python framework connected to a Databricks RAG endpoint.

The chatbot is designed to demonstrate how an enterprise RAG agent can be exposed through a simple, user-friendly web interface.

## Tech Stack

| Layer                  | Technology                                |
| ---------------------- | ----------------------------------------- |
| Frontend               | Chainlit                                  |
| Backend                | Python                                    |
| AI Endpoint            | Databricks Model Serving                  |
| Database               | SQLite                                    |
| Authentication         | Chainlit password authentication for demo |
| Environment Management | python-dotenv                             |
| Version Control        | Git and GitHub                            |

## Key Features

* Chat interface connected to Databricks RAG endpoint
* SQLite-based conversation history
* Multiple users through demo login
* Multiple conversations per user
* Ability to load previous conversations
* User feedback using Helpful / Not Helpful buttons
* Export current conversation as a `.txt` file
* Copy/save response using Chainlit built-in message controls
* Dark/light mode support through Chainlit
* Mobile responsive UI through Chainlit
* Basic app branding through Chainlit configuration

## Architecture

```text
User
  |
  v
Chainlit Chat UI
  |
  v
Python Application
  |
  +--> SQLite Database
  |      - users
  |      - conversations
  |      - messages
  |      - feedback
  |
  v
Databricks Model Serving Endpoint
  |
  v
RAG Agent Response
```

## Project Structure

```text
databricks-rag-chainlit-chatbot/
│
├── app.py
├── databricks_client.py
├── export_utils.py
├── requirements.txt
├── README.md
├── chainlit.md
├── .gitignore
│
├── database/
│   ├── __init__.py
│   ├── connection.py
│   ├── repository.py
│   └── schema.py
│
├── exports/
└── .chainlit/
    └── config.toml
```

## Database Design

The application uses SQLite with the following tables:

```text
users
  - user_id
  - username
  - display_name
  - created_at

conversations
  - conversation_id
  - user_id
  - title
  - created_at
  - last_updated

messages
  - message_id
  - conversation_id
  - sender
  - message
  - created_at

feedback
  - feedback_id
  - message_id
  - rating
  - comment
  - created_at
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd databricks-rag-chainlit-chatbot
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment.

For Windows PowerShell:

```bash
venv\Scripts\Activate.ps1
```

For Windows Command Prompt:

```bash
venv\Scripts\activate.bat
```

For Mac/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

Create a `.env` file in the project root.

```env
DATABRICKS_TOKEN=your_databricks_token_here
DATABRICKS_ENDPOINT_URL=your_databricks_serving_endpoint_url_here
CHAINLIT_AUTH_SECRET=your_chainlit_auth_secret_here
```

To generate the Chainlit auth secret:

```bash
chainlit create-secret
```

### 5. Run the application

```bash
chainlit run app.py
```

Then open the local Chainlit URL in the browser.

## Demo Login

For the class demo, the app uses simple Chainlit password authentication.

```text
Username: any username
Password: demo123
```

Each username is saved as a separate user in SQLite.

In a production version, this temporary login can be replaced with Azure AD or enterprise SSO.

## Current Status

Completed:

* Databricks endpoint connection
* Chainlit chatbot UI
* SQLite database schema
* Conversation persistence
* Multiple users
* Multiple conversations
* Conversation loading
* User feedback
* Conversation export
* Clean response parsing
* Basic app branding

Planned improvements:

* Full Azure AD authentication
* More polished conversation sidebar
* Search previous conversations
* Better admin/reporting view
* Deployment to cloud or internal server

## Notes

The `.env` file is intentionally excluded from Git because it contains secrets.

The local SQLite database and exported conversation files are also excluded from Git.
