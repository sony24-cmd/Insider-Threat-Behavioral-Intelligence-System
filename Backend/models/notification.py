from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from database import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    message = Column(String(500), nullable=False)
    severity = Column(String(50), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)