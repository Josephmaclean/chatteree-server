from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.api import deps
from app.controllers.user_controller import UserController
from app.schemas import user_schema
from app.definitions.service_result import handle_result

router = APIRouter(
    prefix="/user", tags=["users"], responses={404: {"description": "not found"}}
)


@router.post("/", response_model=user_schema.User)
async def create_user(
    user: user_schema.UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(dependency=deps.get_db),
):

    result = await UserController(db, background_tasks=background_tasks).create_user(
        user
    )
    return handle_result(result)


@router.post("/confirm_otp", response_model=user_schema.User)
async def confirm_otp(
    data: user_schema.ConfirmOtp, db: Session = Depends(dependency=deps.get_db)
):
    result = UserController(db).confirm_user(data)
    return handle_result(result)
