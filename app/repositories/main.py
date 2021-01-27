from typing import TypeVar, Any, Dict, Union, Type
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.db import Base

ModelType = TypeVar("ModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=Base)


class DBSessionContext(object):
    def __init__(self, db: Session):
        self.db = db


class BaseRepository(DBSessionContext):
    def __init__(self, db: Session, model: Type[ModelType]):
        super(BaseRepository, self).__init__(db)
        self.model = model

    def create(self, obj_in: Union[SchemaType, Dict[str, Any]]) -> ModelType:
        """
        A wrapper around sqlalchemy create method available to all children of this class
        :param obj_in: SchemaType | Dict - data to be stored in the database
        :return:
        """
        obj_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_data)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def find_by_id(self, id: int) -> ModelType:
        """
        returns a user if it exists in the database
        :param id: int - id of the user
        :return:
        """
        user = self.db.query(self.model).get(id)
        return user

    def update_by_id(
        self, id: int, obj_in: Union[SchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        abstracted function which is inherited automatically. updates
        a model by finding the model by id and updating it with the data passed in via obj_in
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
