from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.api import deps
from app.controllers.user_controller import UserController
from app.schemas import user_schema
from app.schemas import jwt_schema
from app.definitions.service_result import handle_result

router = APIRouter()


@router.post("/", response_model=user_schema.User)
async def create_user(
    user: user_schema.UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(dependency=deps.get_db),
):

    result = UserController(db, background_tasks=background_tasks).authenticate_user(
        user
    )
    return handle_result(result)


@router.post("/confirm_otp", response_model=jwt_schema.Token)
async def confirm_otp(
    data: user_schema.UserConfirmOtp, db: Session = Depends(dependency=deps.get_db)
):
    result = UserController(db).confirm_user(data)
    return handle_result(result)


@router.post("/resend_otp", response_model=user_schema.User)
async def resend_otp(
    id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(dependency=deps.get_db),
):
    result = UserController(db, background_tasks=background_tasks).resend_otp(id)

    return handle_result(result)
