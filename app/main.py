from fastapi import FastAPI
from functools import lru_cache
from app.api.api_v1 import api
from fastapi.exceptions import RequestValidationError
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core import config
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


app.include_router(api.api_router, prefix=get_settings().API_V1_STR)


def get_origins():
    if get_settings().ALLOW_ORIGINS:
        origins = get_settings().ALLOW_ORIGINS
    else:
        origins = ["http://localhost:8000"]

    return origins


app.add_middleware(
    CORSMiddleware,
    allow_origins=get_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
