from sqlalchemy import Boolean, Column, Integer, String, DateTime, sql
from sqlalchemy.orm import relationship
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True)
    image = Column(String)
    is_active = Column(Boolean, default=False, nullable=False)
    otp_code = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=sql.func.now())
    updated_at = Column(DateTime(timezone=True))
