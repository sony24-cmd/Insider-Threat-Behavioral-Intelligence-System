from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import relationship

from database import Base


class Employee(Base):
    __tablename__ = "employees"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Employee Details
    employee_id = Column(String(20), unique=True, nullable=False)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
    )

    department = Column(String(100), nullable=False)
    designation = Column(String(100), nullable=False)
    manager = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    joining_date = Column(Date, nullable=True)

    status = Column(
        String(30),
        default="Active",
        nullable=False,
    )

    # Timestamps
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # ==========================
    # Relationships
    # ==========================

    # One User ↔ One Employee
    user = relationship(
        "User",
        back_populates="employee",
    )

    # One Employee ↔ Many Devices
    devices = relationship(
        "Device",
        back_populates="employee",
        cascade="all, delete-orphan",
    )

    # ----------------------------------------------------
    # AccessPrivilege model has NOT been created yet.
    # Uncomment this relationship after creating:
    # Backend/models/access_privilege.py
    # ----------------------------------------------------

    # privileges = relationship(
    #     "AccessPrivilege",
    #     back_populates="employee",
    #     cascade="all, delete-orphan",
    # )