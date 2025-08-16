from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from src.db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email= Column(String, unique=True, index=True)
    password_hash = Column(String, nullable=True) #Social users can be null
    is_verified = Column(Boolean, default=False)
    provider = Column(String, default="local")  # local | google | github etc
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    upadated_at = Column(DateTime(timezone=True), onupdate=func.now())
