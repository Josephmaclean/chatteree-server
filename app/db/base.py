from sqlalchemy.ext.declarative import as_declarative, declared_attr
from typing import Any


@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate tablename automatically
    @declared_attr
    def __tablename__(self) -> str:
        return self.__tablename__.lower()
