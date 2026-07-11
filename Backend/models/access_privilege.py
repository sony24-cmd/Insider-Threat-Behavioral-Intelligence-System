from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class AccessPrivilege(Base):
    __tablename__ = "access_privileges"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(
        Integer,
        ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False,
    )

    resource_name = Column(String(100), nullable=False)

    access_level = Column(String(50), nullable=False)

    granted_by = Column(String(100), nullable=False)

    expiry_date = Column(Date)

    status = Column(
        String(30),
        default="Active"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    employee = relationship(
        "Employee",
        back_populates="privileges"
    )