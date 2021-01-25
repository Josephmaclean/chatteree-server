from sqlalchemy.orm import Session
from fastapi import BackgroundTasks


class DBSessionContext(object):
    def __init__(self, db: Session):
        self.db = db


class AppController(DBSessionContext):
    def __init__(self, db: Session, background_tasks: BackgroundTasks = None):
        super(AppController, self).__init__(db)
        if background_tasks:
            self.background_tasks = background_tasks
