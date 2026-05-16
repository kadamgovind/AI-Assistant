from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from groq import Groq

# 🔹 DB Imports
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models

# ✅ Create tables
Base.metadata.create_all(bind=engine)

# ✅ Load env
load_dotenv()

# ✅ Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ✅ App
app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# 🔹 DB Dependency
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------
# 📦 Request Models
# -----------------------------
class ChatRequest(BaseModel):
    user_id: int
    message: str

class Query(BaseModel):
    question: str

class UserCreate(BaseModel):
    name: str
    email: str

# -----------------------------
# 🏠 Home
# -----------------------------
@app.get("/")
def home():
    return {"message": "AI Assistant Backend Running 🚀"}

# -----------------------------
# 🆕 Signup (Best Practice)
# -----------------------------
@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):

    # 👉 Check if email already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()

    if existing_user:
        return {"error": "Email already registered ❌"}

    # 👉 Create user
    new_user = models.User(
        name=user.name,
        email=user.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully ✅",
        "user_id": new_user.id
    }

# -----------------------------
# 👥 Get Users
# -----------------------------
@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

# -----------------------------
# 💬 CHAT (User-wise Memory)
# -----------------------------
@app.post("/chat")
async def chat(req: ChatRequest, db: Session = Depends(get_db)):
    try:
        user_id = req.user_id
        user_message = req.message

        # 👉 Save user message
        user_msg = models.ChatMessage(
            user_id=user_id,
            role="user",
            content=user_message
        )
        db.add(user_msg)
        db.commit()

        # 👉 Get this user's chat history
        history = db.query(models.ChatMessage)\
                    .filter(models.ChatMessage.user_id == user_id)\
                    .all()

        messages = [
            {"role": "system", "content": "You are Ava, a smart AI assistant."}
        ]

        for msg in history:
            messages.append({
                "role": msg.role,
                "content": msg.content
            })

        # 👉 AI response
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages
        )

        reply = completion.choices[0].message.content

        # 👉 Save AI reply
        ai_msg = models.ChatMessage(
            user_id=user_id,
            role="assistant",
            content=reply
        )
        db.add(ai_msg)
        db.commit()

        return {"response": reply}

    except Exception as e:
        return {"error": str(e)}

# -----------------------------
# ❓ Quick Ask (No Memory)
# -----------------------------
@app.post("/ask")
def ask_ai(query: Query):
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": query.question}
            ]
        )

        return {"answer": completion.choices[0].message.content}

    except Exception as e:
        return {"error": str(e)}

# -----------------------------
# 🧹 Clear Chat
# -----------------------------
@app.delete("/clear/{user_id}")
def clear_chat(user_id: int, db: Session = Depends(get_db)):
    db.query(models.ChatMessage)\
      .filter(models.ChatMessage.user_id == user_id)\
      .delete()

    db.commit()

    return {"message": f"Chat cleared for user {user_id} 🧹"}