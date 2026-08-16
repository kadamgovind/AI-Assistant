from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from groq import Groq
from sqlalchemy.orm import Session

# DB
from database import SessionLocal, engine, Base
import models

# Voice router
from voice import router as voice_router

# Security
from passlib.context import CryptContext

# -----------------------------
# ENV LOAD
# -----------------------------
load_dotenv()

# -----------------------------
# DB INIT
# -----------------------------
Base.metadata.create_all(bind=engine)

# -----------------------------
# APP INIT
# -----------------------------
app = FastAPI(title="AIRA AI Assistant 🚀")

# -----------------------------
# PASSWORD HASHING
# -----------------------------
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

# -----------------------------
# GROQ CLIENT
# -----------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise Exception("❌ GROQ_API_KEY missing in .env")

client = Groq(api_key=GROQ_API_KEY)

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# ROUTERS
# -----------------------------
app.include_router(voice_router)

# -----------------------------
# DB SESSION
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------
# SCHEMAS
# -----------------------------
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class ChatRequest(BaseModel):
    user_id: int
    message: str

class Query(BaseModel):
    question: str

# -----------------------------
# HOME
# -----------------------------
@app.get("/")
def home():
    return {"message": "AIRA Backend Running 🚀"}

# -----------------------------
# SIGNUP
# -----------------------------
@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()

    if existing:
        raise HTTPException(status_code=400, detail="Email already registered ❌")

    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created ✅", "user_id": new_user.id}

# -----------------------------
# LOGIN
# -----------------------------
@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="User not found ❌")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid password ❌")

    return {
        "message": "Login successful ✅",
        "user_id": db_user.id
    }

# -----------------------------
# GET USERS
# -----------------------------
@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

# -----------------------------
# CHAT WITH MEMORY
# -----------------------------
@app.post("/chat")
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter(models.User.id == req.user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found ❌")

        db.add(models.ChatMessage(
            user_id=req.user_id,
            role="user",
            content=req.message
        ))
        db.commit()

        history = db.query(models.ChatMessage)\
            .filter(models.ChatMessage.user_id == req.user_id)\
            .order_by(models.ChatMessage.id.desc())\
            .limit(10)\
            .all()

        history.reverse()

        messages = [{
            "role": "system",
            "content": "You are Aira AI assistant. Keep responses short and helpful."
        }]

        for msg in history:
            messages.append({
                "role": msg.role,
                "content": msg.content
            })

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages
        )

        reply = completion.choices[0].message.content

        db.add(models.ChatMessage(
            user_id=req.user_id,
            role="assistant",
            content=reply
        ))
        db.commit()

        return {"response": reply}

    except Exception as e:
        print("CHAT ERROR:", str(e))
        raise HTTPException(status_code=500, detail="Chat failed ❌")

# -----------------------------
# ASK (NO MEMORY)
# -----------------------------
@app.post("/ask")
def ask_ai(query: Query):
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": query.question}]
        )

        return {"answer": completion.choices[0].message.content}

    except Exception as e:
        print("ASK ERROR:", str(e))
        raise HTTPException(status_code=500, detail="AI request failed ❌")

# -----------------------------
# CLEAR CHAT
# -----------------------------
@app.delete("/clear/{user_id}")
def clear_chat(user_id: int, db: Session = Depends(get_db)):
    deleted = db.query(models.ChatMessage)\
        .filter(models.ChatMessage.user_id == user_id)\
        .delete()

    db.commit()

    return {
        "message": "Chat cleared 🧹",
        "deleted_messages": deleted
    }