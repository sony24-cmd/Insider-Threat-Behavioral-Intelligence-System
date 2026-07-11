from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class RiskScoreBase(BaseModel):
    employee_id: int
    risk_score: float
    risk_level: str
    remarks: Optional[str] = None


class RiskScoreCreate(RiskScoreBase):
    pass


class RiskScoreUpdate(BaseModel):
    risk_score: Optional[float] = None
    risk_level: Optional[str] = None
    remarks: Optional[str] = None


class RiskScoreResponse(RiskScoreBase):
    id: int
    calculated_on: datetime

    class Config:
        from_attributes = True