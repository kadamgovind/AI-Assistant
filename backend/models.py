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

    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    # 🔗 Relationship with chat messages
    messages = relationship(
        "ChatMessage",
        back_populates="user",
        cascade="all, delete-orphan",   # ✅ FIXED (best practice)
        passive_deletes=True            # ✅ IMPORTANT for CASCADE
    )

    def __repr__(self):
        return f"<User id={self.id} email={self.email}>"

# -----------------------------
# 💬 Chat Messages Table
# -----------------------------
class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),  # ✅ correct
        nullable=False,
        index=True
    )

    role = Column(String(20), nullable=False)   # "user" / "assistant"
    content = Column(Text, nullable=False)

    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    # 🔗 Relationship back to user
    user = relationship(
        "User",
        back_populates="messages"
    )

    def __repr__(self):
        return f"<ChatMessage id={self.id} user_id={self.user_id} role={self.role}>"