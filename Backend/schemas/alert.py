from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# ==========================
# Base Schema
# ==========================

class AlertBase(BaseModel):
    employee_id: int
    risk_score_id: int
    alert_type: str
    severity: str
    description: str
    status: str = "Open"


# ==========================
# Create Schema
# ==========================

class AlertCreate(AlertBase):
    pass


# ==========================
# Update Schema
# ==========================

class AlertUpdate(BaseModel):
    alert_type: Optional[str] = None
    severity: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    resolved_at: Optional[datetime] = None


# ==========================
# Response Schema
# ==========================

class AlertResponse(AlertBase):
    id: int
    generated_at: datetime
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True