from functools import lru_cache
from typing import Generator

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette import status

from app import config, security, models, schemas
from app.config import settings
from app.db.session import SessionLocal
from app.definitions.app_exceptions import AppException
from app.definitions.service_result import ServiceResult
from app.repositories.user_repository import UserRepository


# reusable_oauth2 = OAuth2PasswordBearer(
#     tokenUrl=f"{settings.API_V1_STR}/users/confirm_otp"
# )


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class DecodeToken:
    def __init__(self, token: str):
        self.token = token

    def __call__(self, token: str = "", db: Session = Depends(get_db)):
        try:
            payload = jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms=[security.token.ALGORITHM]
            )
            token_data = schemas.token_schema.TokenData(**payload)
        except (jwt.JWTError, ValidationError) as e:
            print(e)
            raise AppException.Unauthorized(
                context={"message": "Could not validate credential"}
            )
        user = UserRepository(db).find_by_id(token_data.sub)
        if not user:
            raise AppException.ResourceDoesNotExist(
                context={"message": "user not found"}
            )

        if not UserRepository(db).is_active(user):
            raise AppException.Unauthorized(context={"message": "user is inactive"})
        return user
