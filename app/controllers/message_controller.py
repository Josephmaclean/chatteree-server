from main import AppController
from sqlalchemy.orm import Session
from fastapi import BackgroundTasks


class MessageController(AppController):
    def send_message(self, current_user):
        pass
