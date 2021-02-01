from fastapi import APIRouter, Header, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.controllers.message_controller import MessageController
from app.definitions.service_result import handle_result
from app.schemas import user_schema, message_schema

router = APIRouter()


@router.post("/")
def create_message(
    message: message_schema.MessageCreate,
    db: Session = Depends(deps.get_db),
    current_user: user_schema.User = Depends(deps.DecodeToken(Header(None))),
):
    result = MessageController(db).send_message(current_user, message)
    handle_result(result)
