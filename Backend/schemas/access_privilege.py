from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AccessPrivilegeBase(BaseModel):
    employee_id: int
    resource_name: str
    access_level: str
    granted_by: str
    status: str = "Active"


class AccessPrivilegeCreate(AccessPrivilegeBase):
    pass


class AccessPrivilegeUpdate(BaseModel):
    resource_name: Optional[str] = None
    access_level: Optional[str] = None
    granted_by: Optional[str] = None
    status: Optional[str] = None


class AccessPrivilegeResponse(AccessPrivilegeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True