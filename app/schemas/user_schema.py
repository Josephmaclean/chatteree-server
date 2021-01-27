from datetime import datetime, timedelta, date, time
from typing import List, Optional

from pydantic import BaseModel, Field, EmailStr


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    is_active: Optional[bool] = False
    image: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr


class UserUpdate(UserBase):
    username: Optional[str] = Field(
        min_length=2, description="length of username should be greater than 2"
    )


class ConfirmOtp(BaseModel):
    email: EmailStr
    otp_code: str


class UserInDbBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# additional properties stored in DB
class UserInDb(UserInDbBase):
    created_at: datetime
    updated_at: datetime


# additional properties to return via API
class User(UserInDbBase):
    pass
