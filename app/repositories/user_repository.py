import random
from .main import AppRepository
from app.schemas.user_schema import UserCreate, User
from app.models import user_model


class UserRepository(AppRepository):
    __instance = None

    # def __init__(self):
    #     super(UserRepository, self).__init__(db)

    def create_user(self, user: UserCreate) -> User:
        otp_code = str(random.randint(100000, 999999))
        otp_code = otp_code
        user = user_model.User(
            email=user.email, otp_code=otp_code, username=user.username, is_active=False
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_email(self, email: str) -> User:
        return (
            self.db.query(user_model.User).filter(user_model.User.email == email).first()
        )

    def edit_user(self, email: str) -> None:
        self.db.query(user_model.User).filter(user_model.User.email == email).update(
            {user_model.User.is_active: True, user_model.User.otp_code: ""},
            synchronize_session=False,
        )
        self.db.commit()
