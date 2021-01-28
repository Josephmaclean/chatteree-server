from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.enums import MessageTypeEnum
from app.schemas.user_schema import UserInDbBase


class MessageBase(BaseModel):
    type: Optional[MessageTypeEnum] = None
    content: Optional[str] = None
    sender_id: Optional[int] = None
    chatroom_id: Optional[int] = None


class MessageInDbBase(MessageBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class MessageInDb(MessageInDbBase):
    created_at: datetime
    deleted_at: datetime


class MessageWithSender(MessageInDbBase):
    sender = [UserInDbBase]
