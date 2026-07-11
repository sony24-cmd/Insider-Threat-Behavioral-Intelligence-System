from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=False
    )

    activity_type = Column(String, nullable=False)

    description = Column(String, nullable=False)

    ip_address = Column(String, nullable=True)

    device_name = Column(String, nullable=True)

    risk_level = Column(String, default="Low")

    timestamp = Column(DateTime, default=datetime.utcnow)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    employee = relationship(
        "Employee",
        back_populates="activity_logs"
    )