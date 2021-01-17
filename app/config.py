from fastapi import FastAPI
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Chatteree API"
    admin_email: str

    class Config:
        env_file = ".env"