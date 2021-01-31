import random
from datetime import timedelta, datetime
from typing import Optional, Dict, Union
from fastapi.encoders import jsonable_encoder

from app.schemas.user_schema import UserCreate, UserConfirmOtp
from app.controllers.main import AppController
from app.definitions.service_result import ServiceResult
from app.repositories.user_repository import UserRepository
from app.definitions.app_exceptions import AppException
from app.security.token import create_access_token
from app.services.email_service import EmailService
from app.config import settings


class UserController(AppController):
    def authenticate_user(self, user: UserCreate) -> ServiceResult:
        user_repository = UserRepository(self.db)

        token = random.randint(100000, 999999)
        db_user = user_repository.get_user_by_email(user.email)
        if db_user:
            user = user_repository.update_by_id(db_user.id, {"otp_code": token})
            self.send_auth_email(user)
            return ServiceResult(db_user)

        obj_data = jsonable_encoder(user)
        obj_data["otp_code"] = token
        user = user_repository.create(obj_data)

        self.send_auth_email(user)

        return ServiceResult(user)

    def send_mail(self, email, subject, message):
        EmailService().send_mail(email, subject, message)

    def confirm_user(self, data: Union[UserConfirmOtp, Dict]):
        if isinstance(data, dict):
            db_data = data
        else:
            db_data = data.dict()

        db_user = UserRepository(self.db).find_by_id(db_data["id"])

        if not db_user:
            return ServiceResult(
                AppException.ResourceDoesNotExist(
                    context={"success": False, "message": "user does not exist"}
                )
            )
        otp_code = db_user.otp_code

        if otp_code != db_data["otp_code"]:
            return ServiceResult(
                AppException.Unauthorized(context={"message": "Wrong code"})
            )

        else:
            return self.login_user(db_user)

    def login_user(self, db_user) -> ServiceResult:
        UserRepository(self.db).update_by_id(
            db_user.id, {"otp_code": "", "is_active": True}
        )
        access_token = create_access_token(
            data={"sub": str(db_user.id)},
            expires_at=timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        return ServiceResult({"access_token": access_token, "token_type": "bearer"})

    def generate_otp(self) -> int:
        return random.randint(100000, 999999)

    def resend_otp(self, id: int):
        user_repository = UserRepository(self.db)

        db_user = user_repository.find_by_id(id)

        if not db_user:
            return ServiceResult(AppException.Unauthorized())

        otp_code = self.generate_otp()
        db_user = user_repository.update_by_id(id, {"otp_code": otp_code})

        self.send_auth_email(db_user)

        return ServiceResult(db_user)

    def send_auth_email(self, db_user):
        message = f"your one time pin is {db_user.otp_code}"
        email = db_user.email
        subject = "Please confirm your email address"
        self.background_tasks.add_task(self.send_mail, email, subject, message)
