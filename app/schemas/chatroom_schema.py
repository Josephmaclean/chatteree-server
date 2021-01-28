from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.user_schema import UserInDbBase


class BaseChatroom(BaseModel):
    description: Optional[str] = None
    image: Optional[str] = None
    is_group_chat: Optional[str] = None


class ChatroomInDbBase(BaseChatroom):
    id: int

    class Config:
        orm_mode = True


class ChatroomInDb(ChatroomInDbBase):
    created_at: datetime


class Chatroom(ChatroomInDbBase):
    pass


class ChatroomWithUsers(ChatroomInDbBase):
    users = [UserInDbBase]
