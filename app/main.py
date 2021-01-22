from fastapi import FastAPI
from app.api.routes import users
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import  HTTPException as StarletteHttpException
from app.db.session import SessionLocal, engine
from app.models import user_model
from app.definitions.app_exceptions import *


# user_model.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def custom_app_exception_handler(request, e):
    return await app_exception_handler(request, e)


app.include_router(users.router)
