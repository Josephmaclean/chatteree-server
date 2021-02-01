from app.controllers.main import AppController
from app.schemas import chatroom_schema


class ChatroomController(AppController):
    def create(self, obj_in: chatroom_schema.ChatroomCreate):
        pass
        # if obj_in.is_group_chat:
        # group_name = obj_in.name
