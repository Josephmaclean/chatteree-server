from fastapi import FastAPI
from functools import lru_cache
from app.api.routes import users
from fastapi.exceptions import RequestValidationError
from fastapi.exceptions import HTTPException
from app import config
from app.definitions.app_exceptions import app_exception_handler, AppExceptionCase


@lru_cache
def get_settings():
    return config.Settings()


app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, e):
    return await app_exception_handler(request, e)


@app.exception_handler(AppExceptionCase)
async def custom_app_exception_handler(request, e):
    return await app_exception_handler(request, e)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, e):
    return await app_exception_handler(request, e)


app.include_router(users.router)
