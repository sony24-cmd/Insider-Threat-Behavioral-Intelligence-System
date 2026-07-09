from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class EmployeeBase(BaseModel):
    employee_id: str
    department: str
    designation: str
    manager: Optional[str] = None
    phone: Optional[str] = None
    joining_date: Optional[date] = None
    status: str = "Active"


class EmployeeCreate(EmployeeBase):
    user_id: int


class EmployeeUpdate(BaseModel):
    department: Optional[str] = None
    designation: Optional[str] = None
    manager: Optional[str] = None
    phone: Optional[str] = None
    joining_date: Optional[date] = None
    status: Optional[str] = None


class EmployeeResponse(EmployeeBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True