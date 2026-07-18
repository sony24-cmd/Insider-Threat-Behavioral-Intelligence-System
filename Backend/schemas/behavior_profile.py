from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BehaviorProfileBase(BaseModel):
    employee_id: int
    avg_login_hour: float
    avg_logout_hour: float
    avg_daily_logins: float
    avg_file_access: float
    avg_usb_usage: float
    avg_network_usage: float
    avg_device_switches: float
    baseline_risk: str


class BehaviorProfileCreate(BehaviorProfileBase):
    pass


class BehaviorProfileUpdate(BaseModel):
    avg_login_hour: Optional[float] = None
    avg_logout_hour: Optional[float] = None
    avg_daily_logins: Optional[float] = None
    avg_file_access: Optional[float] = None
    avg_usb_usage: Optional[float] = None
    avg_network_usage: Optional[float] = None
    avg_device_switches: Optional[float] = None
    baseline_risk: Optional[str] = None


class BehaviorProfileResponse(BehaviorProfileBase):
    id: int
    last_updated: datetime

    class Config:
        from_attributes = True