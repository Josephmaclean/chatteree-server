from typing import List, Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    username: str


class UserCreate(UserBase):
    otp_code: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True