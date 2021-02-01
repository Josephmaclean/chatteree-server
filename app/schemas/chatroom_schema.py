from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator

from app.schemas.user_schema import UserInDbBase


class ChatroomBase(BaseModel):
    description: Optional[str] = None
    image: Optional[str] = None
    is_group_chat: Optional[bool] = None


class ChatroomInDbBase(ChatroomBase):
    id: int

    class Config:
        orm_mode = True


class ChatroomInDb(ChatroomInDbBase):
    created_at: datetime


class ChatroomCreate(ChatroomBase):
    is_group_chat: bool = False

    # @validator()


class Chatroom(ChatroomInDbBase):
    pass


class ChatroomWithUsers(ChatroomInDbBase):
    users = [UserInDbBase]
