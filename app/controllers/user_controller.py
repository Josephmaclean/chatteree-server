from starlette.exceptions import HTTPException
from app.schemas.user_schema import UserCreate
from app.controllers.main import AppController
from app.definitions.service_result import ServiceResult
from app.repositories.user_repository import UserRepository
from app.definitions.app_exceptions import AppException


class UserController(AppController):
    def create_user(self, user: UserCreate) -> ServiceResult:
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
        return user
