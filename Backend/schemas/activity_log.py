from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ActivityLogBase(BaseModel):
    employee_id: int
    activity_type: str
    description: str
    ip_address: Optional[str] = None
    device_name: Optional[str] = None
    risk_level: str = "Low"


class ActivityLogCreate(ActivityLogBase):
    pass


class ActivityLogUpdate(BaseModel):
    activity_type: Optional[str] = None
    description: Optional[str] = None
    ip_address: Optional[str] = None
    device_name: Optional[str] = None
    risk_level: Optional[str] = None


class ActivityLogResponse(ActivityLogBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
