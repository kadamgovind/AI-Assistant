🤖 AI Assistant

«An AI-powered personal assistant built with Python, FastAPI, Groq AI, and a database-backed conversational memory system.»

AI Assistant is a full-stack intelligent assistant designed to provide conversational AI interactions through a modern web application.

The project uses a React-based frontend and a FastAPI backend. The backend integrates with Groq AI using the "llama-3.1-8b-instant" model and stores users and conversation history in a database using SQLAlchemy.

---

✨ Features

🧠 AI Chat

- AI-powered conversational interaction
- Natural-language question answering
- Real-time backend API processing
- Powered by Groq AI
- Uses the "llama-3.1-8b-instant" model

💬 Conversation Memory

AI Assistant supports user-specific conversation history.

When a user sends a message:

1. The user message is stored in the database.
2. Previous messages belonging to that user are retrieved.
3. The conversation history is sent to the AI model.
4. The AI generates a response.
5. The AI response is stored in the database.
6. The response is returned to the frontend.

This provides a foundation for persistent conversational memory.

👤 User Management

The backend provides user creation functionality through the "/signup" endpoint.

Users are represented in the database with information such as:

- User ID
- Name
- Email
- Password

The user model is connected to chat messages through a database relationship.

⚡ Quick AI Ask

The "/ask" endpoint allows a user to send a question directly to the AI without using the stored conversation history.

This is useful for standalone questions and quick AI interactions.

🧹 Clear Conversation

Users can clear their stored conversation history using:

DELETE /clear/{user_id}

This removes chat messages associated with the specified user.

---

🏗️ Architecture

                    ┌──────────────────────┐
                    │        User          │
                    │                      │
                    │  Chat / Questions    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Frontend        │
                    │   Web Application    │
                    └──────────┬───────────┘
                               │
                         HTTP / API
                               │
                               ▼
                    ┌──────────────────────┐
                    │       FastAPI        │
                    │       Backend        │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
       │  Groq AI    │  │  Database   │  │    Users    │
       │             │  │             │  │             │
       │ Llama 3.1   │  │ SQLAlchemy  │  │ User Data   │
       │ 8B Instant  │  │ Chat History│  │             │
       └─────────────┘  └─────────────┘  └─────────────┘

---

📁 Project Structure

AI-Assistant/
│
├── backend/
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── requirements.txt
│   └── .gitignore
│
├── frontend/
│   └── ...
│
└── README.md

The backend currently contains the FastAPI application, database configuration, SQLAlchemy models, dependency list, and backend-specific Git configuration.

---

⚙️ Backend

The backend is built with FastAPI.

It provides API endpoints for:

- Health/status checking
- User signup
- User retrieval
- AI chat
- Quick AI questions
- Conversation deletion

The main FastAPI application is implemented in:

backend/main.py

---

🔌 API Endpoints

🏠 Home

GET /

Returns a simple backend status response indicating that the AI Assistant backend is running.

---

👤 Signup

POST /signup

Creates a new user.

Example request:

{
  "name": "John",
  "email": "john@example.com"
}

The backend checks whether the email already exists before creating the user.

---

👥 Get Users

GET /users/

Returns users stored in the database.

---

💬 Chat

POST /chat

Example request:

{
  "user_id": 1,
  "message": "Explain artificial intelligence."
}

The endpoint:

- Saves the user's message.
- Retrieves the user's previous conversation.
- Sends the conversation to the AI model.
- Generates an AI response.
- Saves the AI response.
- Returns the response to the client.

---

❓ Quick Ask

POST /ask

Example:

{
  "question": "What is machine learning?"
}

This endpoint sends the question directly to the AI model without using the stored conversation history.

---

🧹 Clear Chat

DELETE /clear/{user_id}

Example:

DELETE /clear/1

Deletes chat messages associated with the specified user.

---

🤖 AI Model

The backend uses Groq as the AI inference provider.

The configured model is:

llama-3.1-8b-instant

The Groq client is initialized using an environment variable:

GROQ_API_KEY

This keeps the API credential outside the source code.

---

🗄️ Database

The project uses SQLAlchemy for database interaction.

The database connection is configured through:

DATABASE_URL

The backend loads the database URL from environment variables and creates a SQLAlchemy engine and session factory.

User Model

The user table contains:

id
name
email
password

Chat Message Model

The chat message table contains:

id
user_id
role
content
timestamp

Chat messages are associated with users through a database relationship.

---

🛠️ Technology Stack

Component| Technology
Frontend| React
Backend| FastAPI
Programming Language| Python
AI Provider| Groq
AI Model| Llama 3.1 8B Instant
Database ORM| SQLAlchemy
Data Validation| Pydantic
Server| Uvicorn
Environment Management| python-dotenv
API Communication| REST

The backend dependency file confirms FastAPI, Uvicorn, Pydantic, "python-dotenv", and related packages.

---

🚀 Getting Started

1. Clone the Repository

git clone https://github.com/kadamgovind/AI-Assistant.git
cd AI-Assistant

---

🐍 Backend Setup

Move into the backend directory:

cd backend

Create a virtual environment:

Windows

python -m venv venv
venv\Scripts\activate

macOS / Linux

python3 -m venv venv
source venv/bin/activate

---

📦 Install Dependencies

pip install -r requirements.txt

The repository contains a backend "requirements.txt" with the Python dependencies used by the application.

---

🔐 Environment Variables

Create a ".env" file inside the "backend" directory.

GROQ_API_KEY=your_groq_api_key
DATABASE_URL=your_database_url

The backend loads these values through "python-dotenv".

⚠️ Security

Never upload your real API keys or database credentials to GitHub.

Do not commit:

.env
API keys
Database passwords
Access tokens
Private credentials

Use ".gitignore" to keep secrets out of the repository.

---

▶️ Run the Backend

From the "backend" directory:

uvicorn main:app --reload

The FastAPI development server will start locally.

You can then access the API through the local server URL.

FastAPI also provides interactive API documentation when the server is running.

---

🌐 Frontend

The project includes a separate "frontend" application.

The frontend communicates with the FastAPI backend to provide the user-facing AI Assistant experience.

frontend/

The frontend can be developed and run independently from the backend.

---

🔄 Application Workflow

User
  │
  ▼
Frontend
  │
  ▼
POST /chat
  │
  ▼
FastAPI Backend
  │
  ├──────────────► Database
  │                    │
  │                    └── Previous Chat History
  │
  ▼
Groq AI
  │
  ▼
Llama 3.1 8B Instant
  │
  ▼
AI Response
  │
  ├──────────────► Database
  │
  ▼
Frontend
  │
  ▼
User

---

🎯 Use Cases

AI Assistant can be used as a foundation for:

- Personal AI assistants
- Conversational AI applications
- AI chatbots
- Customer-support assistants
- Educational assistants
- Productivity assistants
- AI-powered web applications
- Persistent-memory chatbot systems

---

🔮 Future Improvements

Potential improvements include:

- [ ] Secure user authentication
- [ ] Password hashing
- [ ] JWT-based authentication
- [ ] Better session management
- [ ] Streaming AI responses
- [ ] Voice input
- [ ] Text-to-speech
- [ ] Image understanding
- [ ] File/document analysis
- [ ] Web search integration
- [ ] Conversation export
- [ ] Conversation titles
- [ ] User profile management
- [ ] Improved error handling
- [ ] Automated tests
- [ ] API rate limiting
- [ ] Production deployment
- [ ] Docker support
- [ ] CI/CD pipeline

---

⚠️ Security Notes

This project is intended as a development/portfolio project.

Before using it in production, security improvements should be implemented.

In particular:

- Passwords should be securely hashed before storage.
- Authentication and authorization should be added.
- CORS should be restricted to trusted frontend origins.
- API rate limiting should be implemented.
- Database credentials should remain private.
- API keys should always be stored in environment variables.
- Input validation and error handling should be strengthened.

---

📌 Project Status

Status: 🚧 Active Development

The current version provides a full-stack foundation for an AI conversational assistant with:

- React frontend
- FastAPI backend
- Groq-powered AI responses
- User management
- Database persistence
- User-specific chat history
- Quick AI queries
- Chat history deletion

---

👨‍💻 Author

Govind Kadam

GitHub:
https://github.com/kadamgovind

Project Repository:
https://github.com/kadamgovind/AI-Assistant

---

⭐ Contributing

Contributions and suggestions are welcome.

If you want to improve the project:

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Test the changes.
5. Commit your changes.
6. Create a pull request.

---

📄 License

This project currently does not specify a license.

If you plan to distribute the project as open source, add an appropriate license such as the MIT License.

