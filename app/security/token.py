from datetime import datetime, timedelta
from typing import Optional

from jose import jwt

from app.config import settings

ALGORITHM = settings.JWT_ALGORITHM
SECRET_KEY = settings.JWT_SECRET_KEY


def create_access_token(data: dict, expires_at: Optional[timedelta] = None) -> str:

    to_encode = data.copy()
    if expires_at:
        expire = datetime.utcnow() + expires_at
    else:
        expire = datetime.utcnow() + timedelta(minutes=20)

    to_encode.update({"exp": expire, "sub": data["sub"]})
    encoded_jwt = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
