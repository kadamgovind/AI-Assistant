from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

# -----------------------------
# 👤 User Table
# -----------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    password = Column(String, nullable=False)   # ✅ IMPORTANT (login ke liye)

    # 🔗 Relationship with chat messages
    messages = relationship(
        "ChatMessage",
        back_populates="user",
        cascade="all, delete"   # ✅ best practice
    )

# -----------------------------
# 💬 Chat Messages Table
# -----------------------------
class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE")  # ✅ important
    )

    role = Column(String, nullable=False)   # "user" / "assistant"
    content = Column(Text, nullable=False)

    timestamp = Column(DateTime, default=datetime.utcnow)

    # 🔗 Relationship back to user
    user = relationship("User", back_populates="messages")