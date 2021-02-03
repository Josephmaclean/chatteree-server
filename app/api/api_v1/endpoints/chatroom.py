from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from app.api import deps
from app.controllers.chatroom_controller import ChatroomController
from app.definitions.service_result import handle_result
from app.schemas import chatroom_schema

router = APIRouter()


@router.post("/", response_model=chatroom_schema.Chatroom)
def create(
    chatroom: chatroom_schema.ChatroomCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(deps.get_db),
):
    result = ChatroomController(db=db, background_tasks=background_tasks).create(
        chatroom
    )
    return handle_result(result)
