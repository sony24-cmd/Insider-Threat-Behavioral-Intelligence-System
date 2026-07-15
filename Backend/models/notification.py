from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from database import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)

    message = Column(String(500), nullable=False)

    notification_type = Column(String(100), nullable=False)

    status = Column(
        String(50),
        default="Unread",
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )