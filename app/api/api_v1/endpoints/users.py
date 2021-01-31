from fastapi import APIRouter, Depends, BackgroundTasks, Header
from fastapi.params import Form
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.api import deps
from app.controllers.user_controller import UserController
from app.schemas import user_schema
from app.schemas import token_schema
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


@router.post("/confirm_otp", response_model=token_schema.Token)
async def confirm_otp(
    id: int = Form(None, alias="id"),
    otp_code: str = Form(None, alias="otp"),
    db: Session = Depends(dependency=deps.get_db),
):
    data = {"otp_code": otp_code, "id": id}
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


@router.patch("/", response_model=user_schema.User)
async def update_user(
    update_data: user_schema.UserUpdate,
    db: Session = Depends(dependency=deps.get_db),
    current_user: user_schema.User = Depends(deps.DecodeToken(Header(None))),
):
    result = UserController(db).update_user(update_data, current_user)

    return handle_result(result)
