from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.controllers.user_controller import UserController
from app.schemas import user_schema
from app.definitions.service_result import handle_result

router = APIRouter(
    prefix="/user", tags=["users"], responses={404: {"description": "User not found"}}
)


@router.post("/users/", response_model=user_schema.User)
async def create_user(
    user: user_schema.UserCreate, db: Session = Depends(dependency=deps.get_db)
):

    result = UserController(db).create_user(user)
    return handle_result(result)
