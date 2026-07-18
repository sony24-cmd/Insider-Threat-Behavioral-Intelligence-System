from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from database import Base


class BehaviorProfile(Base):
    __tablename__ = "behavior_profiles"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=False,
        unique=True,
    )

    avg_login_hour = Column(Float, default=9.0)
    avg_logout_hour = Column(Float, default=18.0)

    avg_daily_logins = Column(Float, default=1.0)

    avg_file_access = Column(Float, default=20.0)

    avg_usb_usage = Column(Float, default=0.0)

    avg_network_usage = Column(Float, default=100.0)

    avg_device_switches = Column(Float, default=0.0)

    after_hours_activity = Column(Integer, default=0)

    weekend_activity = Column(Integer, default=0)

    behavior_score = Column(Float, default=100.0)

    baseline_risk = Column(
        String(20),
        default="Low",
    )

    last_updated = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    employee = relationship(
        "Employee",
        back_populates="behavior_profile",
    )