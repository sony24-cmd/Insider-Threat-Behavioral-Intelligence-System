from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import relationship

from database import Base


class RiskScore(Base):
    __tablename__ = "risk_scores"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    employee_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=False,
    )

    risk_score = Column(
        Float,
        nullable=False,
    )

    risk_level = Column(
        String(20),
        nullable=False,
    )

    remarks = Column(
        String(255),
        nullable=True,
    )

    calculated_on = Column(
        DateTime,
        default=datetime.utcnow,
    )

    # ==========================
    # Relationships
    # ==========================

    employee = relationship(
        "Employee",
        back_populates="risk_scores",
    )

    alerts = relationship(
        "Alert",
        back_populates="risk_score",
        cascade="all, delete-orphan",
    )