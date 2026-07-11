from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
)

from sqlalchemy.orm import relationship

from database import Base


class Alert(Base):
    __tablename__ = "alerts"

    # ==========================
    # Primary Key
    # ==========================
    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # ==========================
    # Foreign Keys
    # ==========================
    employee_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=False,
    )

    risk_score_id = Column(
        Integer,
        ForeignKey("risk_scores.id"),
        nullable=False,
    )

    # ==========================
    # Alert Details
    # ==========================
    alert_type = Column(
        String(100),
        nullable=False,
    )

    severity = Column(
        String(30),
        nullable=False,
        default="Medium",
    )

    description = Column(
        String(500),
        nullable=False,
    )

    status = Column(
        String(30),
        nullable=False,
        default="Open",
    )

    generated_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    resolved_at = Column(
        DateTime,
        nullable=True,
    )

    # ==========================
    # Relationships
    # ==========================

    employee = relationship(
        "Employee",
        back_populates="alerts",
    )

    risk_score = relationship(
        "RiskScore",
        back_populates="alerts",
    )