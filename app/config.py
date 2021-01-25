from fastapi import FastAPI
from pydantic import BaseSettings


class Settings(BaseSettings):
    db_server: str
    db_user: str
    db_password: str
    db_name: str
    sendgrid_api_key: str

    class Config:
        env_file = ".env"


settings = Settings()
