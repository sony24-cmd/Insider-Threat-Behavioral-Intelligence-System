from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db

from schemas.ai_prediction import (
    AIPredictionRequest,
    AIPredictionResponse,
)

from services.ai_prediction_service import analyze_employee

router = APIRouter(
    prefix="/ai",
    tags=["AI Prediction"],
)


@router.post(
    "/predict-risk",
    response_model=AIPredictionResponse,
)
def predict_employee_risk(
    request: AIPredictionRequest,
    db: Session = Depends(get_db),
):

    return analyze_employee(
        db=db,
        employee_id=request.employee_id,
        login_count=request.login_count,
        logout_count=request.logout_count,
        usb_connect=request.usb_connect,
        usb_disconnect=request.usb_disconnect,
        http_visits=request.http_visits,
        total_events=request.total_events,
    )