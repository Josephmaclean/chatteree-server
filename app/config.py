from fastapi import FastAPI
from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_SERVER: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SENDGRID_API_KEY: str

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
