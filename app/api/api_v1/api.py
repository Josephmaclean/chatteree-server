from fastapi import APIRouter

from app.api.api_v1.endpoints import users, chatroom
from app.api.api_v1.endpoints import messages

api_router = APIRouter()

api_router.include_router(
    users.router,
    prefix="/user",
    tags=["users"],
    responses={404: {"description": "not found"}},
)
api_router.include_router(
    messages.router,
    prefix="/message",
    tags=["messages"],
    responses={404: {"description": "not found"}},
)

api_router.include_router(
    chatroom.router,
    prefix="/chatroom",
    tags=["chatroom"],
    responses={404: {"description": "not found"}},
)
