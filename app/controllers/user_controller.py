import time
import random
from starlette.exceptions import HTTPException
from app.schemas.user_schema import UserCreate, ConfirmOtp
from app.controllers.main import AppController
from app.definitions.service_result import ServiceResult
from app.repositories.user_repository import UserRepository
from app.definitions.app_exceptions import AppException
from app.services.email_service import EmailService


class UserController(AppController):
    async def create_user(self, user: UserCreate) -> ServiceResult:
        user_repository = UserRepository(self.db)

        db_user = user_repository.get_user_by_email(user.email)
        if db_user:
            return ServiceResult(
                AppException.ResourceExists(
                    context={"success": False, "message": "User already exists"}
                )
            )
        user = user_repository.create_user(user)
        if not user:
            return ServiceResult(AppException.CreateResource())

        message = f"your one time pin is {user.otp_code}"
        email = user.email
        subject = "Please confirm your email address"

        self.background_tasks.add_task(self.send_mail, email, subject, message)

        return ServiceResult(user)

    def send_mail(self, email, subject, message):
        EmailService().send_mail(email, subject, message)

    def confirm_user(self, data: ConfirmOtp):
        db_user = UserRepository(self.db).get_user_by_email(data.email)

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
