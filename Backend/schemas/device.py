from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DeviceBase(BaseModel):
    employee_id: int
    device_name: str
    device_type: str
    operating_system: str
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None
    serial_number: str
    status: str = "Assigned"


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(BaseModel):
    device_name: Optional[str] = None
    device_type: Optional[str] = None
    operating_system: Optional[str] = None
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None
    serial_number: Optional[str] = None
    status: Optional[str] = None


class DeviceResponse(DeviceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True