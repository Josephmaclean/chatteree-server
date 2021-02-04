from fastapi.encoders import jsonable_encoder
from typing import Union, Dict, Any
from sqlalchemy.exc import IntegrityError

from app.definitions.app_exceptions import AppException
from app.models.chatroom_model import chatroom_assoc_table
from app.repositories.main import BaseRepository
from app.models import chatroom_model, user_model
from app.schemas import chatroom_schema


class ChatroomRepository(BaseRepository):
    def __init__(self, db):
        super(ChatroomRepository, self).__init__(db, model=chatroom_model.ChatRoom)

    def create_chatroom(
        self, obj_in: Union[chatroom_schema.ChatroomCreate, Dict[str, Any]]
    ):

        decoded_data = jsonable_encoder(obj_in)

        member_ids = decoded_data["members"]
        obj_data = decoded_data.copy()
        del obj_data["members"]

        db_chatroom = chatroom_model.ChatRoom(**obj_data)
        self.db.add(db_chatroom)
        self.db.commit()

        rel_arr = list(map(lambda x: (db_chatroom.id, x), member_ids))
        try:
            self.db.execute(chatroom_assoc_table.insert().values(rel_arr))
            self.db.commit()
            self.db.refresh(db_chatroom)
            return db_chatroom
        except IntegrityError as e:
            raise AppException.ResourceDoesNotExist(context={"message": str(e.orig)})
        except Exception:
            raise AppException.CreateResource()
