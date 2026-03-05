from sqlalchemy import Column, Integer, String, Boolean, DateTime, func

from src.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    login = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(50), unique=True, index=True, nullable=True)
    hashed_password = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=True)
    name = Column(String(50), nullable=True)
    patr = Column(String(50), nullable=True)
    is_admin = Column(Boolean, default=False)
