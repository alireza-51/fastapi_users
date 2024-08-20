from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(50), default="User")  # Role-based access control
    created = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
