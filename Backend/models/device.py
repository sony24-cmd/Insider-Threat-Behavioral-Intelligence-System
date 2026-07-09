from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(
        Integer,
        ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False,
    )

    device_name = Column(String, nullable=False)
    device_type = Column(String, nullable=False)
    operating_system = Column(String, nullable=False)

    ip_address = Column(String, nullable=True)
    mac_address = Column(String, nullable=True)
    serial_number = Column(String, unique=True, nullable=False)

    status = Column(String, default="Assigned")

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationship with Employee
    employee = relationship(
        "Employee",
        back_populates="devices"
    )