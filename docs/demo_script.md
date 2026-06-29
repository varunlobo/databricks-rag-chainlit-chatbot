# Demo Script

## Project Title

Databricks RAG Chainlit Chatbot

## 1. Introduction

This project demonstrates a front-facing chatbot interface built using Chainlit and Python. The chatbot connects to a Databricks Model Serving endpoint that hosts a Retrieval-Augmented Generation, or RAG, agent.

The goal of the project is to provide a simple but functional chatbot UI where users can ask questions, receive answers from the Databricks RAG agent, save conversation history, provide feedback, and export conversations.

## 2. Technology Stack

The application uses:

* Chainlit for the chatbot interface
* Python for backend logic
* Databricks Model Serving for the RAG endpoint
* SQLite for users, conversations, messages, and feedback
* GitHub for version control

## 3. Application Login

The app starts with a simple demo login screen.

For this class project, the login uses Chainlit password authentication.

Demo credentials:

```text
Username: varun
Password: demo123
```

Any username can be used with the demo password. Each username is stored separately in SQLite, which allows the application to demonstrate multi-user conversation history.

In a production version, this temporary login can be replaced with Azure Active Directory or enterprise SSO.

## 4. Chatbot Interaction

After login, the user sees the chatbot interface.

The user can type a question into the chat window. The message is sent from Chainlit to the Python backend, then forwarded to the Databricks Serving endpoint.

The Databricks endpoint returns a response from the RAG agent, and the chatbot displays the cleaned answer in the UI.

At the same time, the application saves:

* the user message
* the assistant response
* the conversation id
* the user id
* timestamps

## 5. Conversation History

The application stores conversation history in SQLite.

When the user logs back in, the app shows previous conversations for that user. The user can select an old conversation and continue chatting.

This demonstrates multiple conversations per user and persistent chat history.

## 6. Feedback

Each assistant response includes feedback buttons:

```text
Helpful
Not Helpful
```

When the user clicks one of these buttons, the feedback is saved in the SQLite feedback table. This can later be used to review answer quality.

## 7. Export Conversation

The user can click:

```text
Export Current Conversation
```

The application retrieves all messages from the current conversation and generates a downloadable `.txt` file.

This allows users to save or share a full conversation transcript.

## 8. Database Design

The SQLite database has four main tables:

```text
users
conversations
messages
feedback
```

The relationship is:

```text
One user can have many conversations.
One conversation can have many messages.
One assistant message can have feedback.
```

## 9. Key Accomplishments

This project successfully implements:

* A Chainlit chatbot interface
* Databricks RAG endpoint integration
* SQLite conversation persistence
* Multiple demo users
* Multiple conversations per user
* Conversation loading
* User feedback
* Conversation export
* Basic branding
* GitHub version control

## 10. Future Improvements

Possible future improvements include:

* Azure AD authentication
* More polished ChatGPT-style sidebar
* Search previous conversations
* Admin dashboard for feedback analytics
* Cloud deployment
* PDF export
* Better role-based access control

## 11. Closing Summary

This project shows how a Databricks RAG agent can be exposed through a Python-based chatbot interface. It combines AI endpoint integration, persistent chat history, feedback capture, and export functionality into a working class project that resembles a lightweight enterprise chatbot.
