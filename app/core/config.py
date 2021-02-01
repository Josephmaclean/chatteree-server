from typing import List

from fastapi import FastAPI
from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    DB_SERVER: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SENDGRID_API_KEY: str
    API_V1_STR: str = "/api/v1"
    EMAILS_FROM_EMAIL: str
    ALLOW_ORIGINS: List[str] = []

    @validator("ALLOW_ORIGINS")
    def check_origins(cls, v):
        """
        returns a list of cross origins as specified with | seperators in environment variables
        :return: List of strings
        """
        if isinstance(v, str):
            return v.strip().split("|")

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
