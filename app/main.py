from fastapi import FastAPI
from app.api.routes import users
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHttpException
from app.definitions.app_exceptions import app_exception_handler, AppExceptionCase


app = FastAPI()


@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(request, e):
    return await app_exception_handler(request, e)


@app.exception_handler(StarletteHttpException)
async def custom_http_exception_handler(request, e):
    return await app_exception_handler(request, e)


@app.exception_handler(AppExceptionCase)
async def custom_app_exception_handler(request, e):
    return await app_exception_handler(request, e)


app.include_router(users.router)
