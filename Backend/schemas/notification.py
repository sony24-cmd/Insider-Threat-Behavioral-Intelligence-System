from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NotificationBase(BaseModel):
    title: str
    message: str
    severity: str


class NotificationCreate(NotificationBase):
    pass


class NotificationUpdate(BaseModel):
    title: Optional[str] = None
    message: Optional[str] = None
    severity: Optional[str] = None


class NotificationResponse(NotificationBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True