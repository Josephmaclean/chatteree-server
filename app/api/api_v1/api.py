from fastapi import APIRouter

from app.api.api_v1.endpoints import users

api_router = APIRouter()

api_router.include_router(
    users.router,
    prefix="/user",
    tags=["users"],
    responses={404: {"description": "not found"}},
)
