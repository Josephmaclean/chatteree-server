from app.controllers.main import AppController
from app.schemas import chatroom_schema


class ChatroomController(AppController):
    def create(self, obj_in: chatroom_schema.ChatroomCreate):
        if obj_in.is_group_chat:
            pass

    # def
