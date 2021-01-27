import random
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from typing import Union, Any, Dict
from .main import BaseRepository
from app.schemas.user_schema import UserCreate, UserInDb, UserUpdate
from app.models import user_model


class UserRepository(BaseRepository):
    __instance = None

    def create_user(self, user: UserCreate) -> UserInDb:

        otp_code = str(random.randint(100000, 999999))
        otp_code = otp_code
        user = user_model.User(
            email=user.email, otp_code=otp_code, username=user.username, is_active=False
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_email(self, email: str) -> UserInDb:
        return (
            self.db.query(user_model.User).filter(user_model.User.email == email).first()
        )

    def find_by_id(self, id: int) -> UserInDb:
        """
        returns user if it exists in the database
        :param id: int - id of the user
        :return:
        """
        return self.db.query(user_model.User).filter(id == id).first()
