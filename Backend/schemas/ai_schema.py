from pydantic import BaseModel


class AIPredictionRequest(BaseModel):
    login_count: int
    logout_count: int
    usb_connect: int
    usb_disconnect: int
    http_visits: int
    total_events: int


class AIPredictionResponse(BaseModel):
    prediction: int
    risk_level: str
    confidence: float