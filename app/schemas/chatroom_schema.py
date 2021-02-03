from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, validator

from app.schemas.user_schema import UserInDbBase


class ChatroomBase(BaseModel):
    name: Optional[str] = None
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
    members: List[int]

    @validator("name")
    def name_exists(cls, v, values, **kwargs):
        if values["is_group_chat"] and len(str(v).strip()) == 0:
            raise ValueError("name is required for a group chat")
        return v


class Chatroom(ChatroomInDbBase):
    pass


class ChatroomWithUsers(ChatroomInDbBase):
    users = [UserInDbBase]
