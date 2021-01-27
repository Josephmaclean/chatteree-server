from typing import TypeVar, Any, Dict, Union
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.db import Base

ModelType = TypeVar("ModelType", bound=Base)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=Base)


class DBSessionContext(object):
    def __init__(self, db: Session):
        self.db = db


class BaseRepository(DBSessionContext):
    def update_by_id(
        self, id: int, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """

        :param id: int - Id of the data you want to update
        :param obj_in: Model instance or dictionary of data you want to update
        :return: UserInDb
        """
        db_obj = self.find_by_id(id)
        obj_data = jsonable_encoder(db_obj)

        if not db_obj:
            raise HTTPException(status_code=400, detail="User does not exits")

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            # exclude unset set to true to remove default values
            update_data = obj_in.dict(exclude_unset=True)

        for field in update_data:
            if field in obj_data:
                setattr(db_obj, field, update_data[field])

        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
