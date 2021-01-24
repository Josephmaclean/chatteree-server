from .main import AppRepository
from app.schemas.user_schema import UserCreate, User
from app.models import user_model


class UserRepository(AppRepository):
    def create_user(self, user: UserCreate) -> User:
        code = "123456"
        user = user_model.User(
            email=user.email, otp_code=code, username=user.username, is_active=False
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_email(self, email: str) -> User:
        return (
            self.db.query(user_model.User).filter(user_model.User.email == email).first()
        )
