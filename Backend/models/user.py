from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    email = Column(String, unique=True, index=True, nullable=False)

    password = Column(String, nullable=False)

    role = Column(String, nullable=False)

    department = Column(String, nullable=True)

    designation = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)