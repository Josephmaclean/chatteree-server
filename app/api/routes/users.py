from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.controllers import user_controller
from app.schemas import user_schema

router = APIRouter()


@router.get("/users/", response_model=user_schema.User)
async def create_user(*, db: Session = Depends(dependency=deps.get_db)):
    return user_controller.create_user(db=db, user=None)
    # return { "message": "The orangutans are three extant species of great apes native to Indonesia and Malaysia." }


