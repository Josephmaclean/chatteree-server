from fastapi.encoders import jsonable_encoder

from app.controllers.main import AppController
from app.definitions.service_result import ServiceResult
from app.repositories.chatroom_repository import ChatroomRepository
from app.schemas import chatroom_schema


class ChatroomController(AppController):
    def create(self, obj_in: chatroom_schema.ChatroomCreate) -> ServiceResult:
        chatroom = ChatroomRepository(self.db).create_chatroom(obj_in=obj_in)
        return ServiceResult(chatroom)
