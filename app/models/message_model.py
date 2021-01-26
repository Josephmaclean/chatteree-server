import enum
import datetime
from sqlalchemy import Column, String, Integer, Enum, DateTime, ForeignKey, sql
from sqlalchemy.orm import relationship
from app.db.base import Base


class MessageTypes(enum.Enum):
    text = 1
    images = 3
    audio = 2
    video = 4
    document = 5


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(MessageTypes), default=MessageTypes.text, nullable=False)
    content = Column(String, nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=sql.func.now())
    deleted_at = Column(DateTime(timezone=True))

    sender = relationship("User", back_populates="messages")
