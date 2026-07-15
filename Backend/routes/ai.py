from fastapi import APIRouter

from schemas.ai_schema import (
    AIPredictionRequest,
    AIPredictionResponse,
)

from services.ai_service import predict_risk

router = APIRouter(
    prefix="/ai",
    tags=["AI Prediction"],
)


# ==========================================
# AI Risk Prediction
# ==========================================

@router.post(
    "/predict-risk",
    response_model=AIPredictionResponse,
)
def predict_employee_risk(
    request: AIPredictionRequest,
):
    result = predict_risk(
        login_count=request.login_count,
        logout_count=request.logout_count,
        usb_connect=request.usb_connect,
        usb_disconnect=request.usb_disconnect,
        http_visits=request.http_visits,
        total_events=request.total_events,
    )

    return result