from datetime import datetime, timedelta
from typing import Optional

from jose import jwt

from app.config import settings


def create_access_token(data: dict, expires_at: Optional[timedelta] = None) -> str:
    secret_key = settings.JWT_SECRET_KEY
    algorithm = settings.JWT_ALGORITHM
    to_encode = data.copy()
    if expires_at:
        expire = datetime.utcnow() + expires_at
    else:
        expire = datetime.utcnow() + timedelta(minutes=20)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(claims=to_encode, key=secret_key, algorithm=algorithm)
    return encoded_jwt
