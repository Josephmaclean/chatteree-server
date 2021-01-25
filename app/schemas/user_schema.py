from typing import List, Optional

from pydantic import BaseModel, Field


# Shared properties
class UserBase(BaseModel):
    email: str
    username: str


# Properties to receive via API on creation
class UserCreate(UserBase):
    # email: str = Field(max_length=)
    username: str = Field(
        min_length=2, description="length of username should be greater than 2"
    )


class ConfirmOtp(BaseModel):
    email: str
    otp_code: str


class UserInDbBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# additional properties stored in DB
class UserInDb(UserInDbBase):
    auth_token: Optional[str] = None


# additional properties to return via API
class User(UserInDbBase):
    pass
