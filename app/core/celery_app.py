from celery import Celery

celery_app = Celery("worker", broker="redis://localhost:6379/")

celery_app.conf.task_routes = {"app.worker.add_chatroom_members": "main-queue"}
