from app.models import user_model
from app.schemas import user_schema
from sqlalchemy.orm import Session


def create_user(db: Session, user: user_schema.UserCreate = None):
    code = "123456"
    user = user_model.User()
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
