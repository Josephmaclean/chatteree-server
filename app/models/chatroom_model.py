from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

association_table = Table(
    "chatroom_users",
    Base.metadata,
    Column("chatroom_id", Integer, ForeignKey("chatrooms.id")),
    Column("user_id", Integer, ForeignKey("users.id")),
)


class ChatRoom(Base):
    __tablename__ = "chatrooms"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    description = Column(String)
    image = Column(String)
    users = relationship("User", secondary=association_table, backref="chatrooms")
