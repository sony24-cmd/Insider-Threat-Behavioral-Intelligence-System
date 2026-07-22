from datetime import datetime

from pydantic import BaseModel


class AnomalyDetectionCreate(BaseModel):
    employee_id: int
    anomaly_score: float
    anomaly_level: str
    reason: str


class AnomalyDetectionResponse(AnomalyDetectionCreate):
    id: int
    detected_at: datetime

    class Config:
        from_attributes = True