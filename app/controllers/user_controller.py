import time
import random
from fastapi.encoders import jsonable_encoder
from starlette.exceptions import HTTPException
from app.schemas.user_schema import UserCreate, UserConfirmOtp
from app.controllers.main import AppController
from app.definitions.service_result import ServiceResult
from app.repositories.user_repository import UserRepository
from app.definitions.app_exceptions import AppException
from app.services.email_service import EmailService


class UserController(AppController):
    async def create_user(self, user: UserCreate) -> ServiceResult:
        user_repository = UserRepository(self.db)

        token = random.randint(100000, 999999)
        db_user = user_repository.get_user_by_email(user.email)
        if db_user:
            user_repository.update_by_id(db_user.id, {"otp_code": token})
            return ServiceResult(db_user)

        obj_data = jsonable_encoder(user)
        obj_data["otp_code"] = token
        user = user_repository.create(obj_data)

        message = f"your one time pin is {user.otp_code}"
        email = user.email
        subject = "Please confirm your email address"

        self.background_tasks.add_task(self.send_mail, email, subject, message)

        return ServiceResult(user)

    def send_mail(self, email, subject, message):
        EmailService().send_mail(email, subject, message)

    def confirm_user(self, data: UserConfirmOtp):
        db_user = UserRepository(self.db).find_by_id(data.id)

        if not db_user:
            return ServiceResult(
                AppException.ResourceDoesNotExist(
                    context={"success": False, "message": "user does not exist"}
                )
            )
        otp_code = db_user.otp_code
        if otp_code == data.otp_code:
            UserRepository(self.db).update_by_id(
                db_user.id, {"otp_code": "", "is_active": True}
            )
            return ServiceResult(db_user)
        else:
            return ServiceResult(
                AppException.Unauthorized(context={"message": "Wrong code"})
            )
