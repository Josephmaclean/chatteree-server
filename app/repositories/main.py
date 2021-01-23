from sqlalchemy.orm import Session


class DBSessionContext(object):
    def __init__(self, db: Session):
        self.db = db


class AppRepository(DBSessionContext):
    pass
