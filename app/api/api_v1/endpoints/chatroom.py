from fastapi import APIRouter, Depends, BackgroundTasks, WebSocket
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session


from app.api import deps
from app.controllers.chatroom_controller import ChatroomController
from app.definitions.service_result import handle_result
from app.schemas import chatroom_schema

router = APIRouter()


# @router.websocket("/ws")
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


@router.websocket("/ws")
async def websocket_create(
    background_tasks: BackgroundTasks,
    web_socket: WebSocket,
    db: Session = Depends(deps.get_db),
):
    await web_socket.accept()
    while True:
        data = await web_socket.receive_json(mode="text")
        obj_in = chatroom_schema.ChatroomCreate(**data)
        result = (
            ChatroomController(db=db, background_tasks=background_tasks)
            .create(obj_in)
            .value
        )

        await web_socket.send_json(jsonable_encoder(result))
