from pydantic import BaseModel


class AIPredictionRequest(BaseModel):
    employee_id: int
    login_count: int
    logout_count: int
    usb_connect: int
    usb_disconnect: int
    http_visits: int
    total_events: int


class AIPredictionResponse(BaseModel):
    risk_id: int
    prediction: int
    confidence: float
    risk_level: str