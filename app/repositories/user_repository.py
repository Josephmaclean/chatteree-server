import random
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from typing import Union, Any, Dict
from .main import BaseRepository
from app.schemas.user_schema import UserCreate, UserInDb, UserUpdate, User
from app.models import user_model


class UserRepository(BaseRepository):
    def __init__(self, db):
        super(UserRepository, self).__init__(db, model=user_model.User)

    def get_user_by_email(self, email: str) -> UserInDb:
        return (
            self.db.query(user_model.User).filter(user_model.User.email == email).first()
        )

    def is_active(self, user: User) -> bool:
        return user.is_active
