from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
)

from database import Base


class AnomalyDetection(Base):
    __tablename__ = "anomaly_detections"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=False,
    )

    anomaly_score = Column(
        Float,
        nullable=False,
    )

    anomaly_level = Column(
        String(30),
        nullable=False,
    )

    reason = Column(
        String(500),
        nullable=False,
    )

    detected_at = Column(
        DateTime,
        default=datetime.utcnow,
    )