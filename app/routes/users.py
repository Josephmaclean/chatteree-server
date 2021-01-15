from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers import user_controller
from app.database import SessionLocal, engine
from app.schemas import user_schema
from app.models import user_model

user_model.Base.metadata.create_all(bind=engine)
router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/users/", tags=["users"])
async def create_user(db: Session = Depends(get_db)):
    return user_controller.create_user(db=db, user=None)
    # return [{"username": "Rick"}, {"username": "Morty"}]




