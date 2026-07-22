from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db

from schemas.anomaly_detection import (
    AnomalyDetectionResponse,
)

from services.anomaly_detection_service import (
    get_all_anomalies,
    get_employee_anomalies,
)


router = APIRouter(
    prefix="/anomalies",
    tags=["Anomaly Detection"],
)


# ==========================================
# Get All Anomalies
# ==========================================

@router.get(
    "/",
    response_model=List[AnomalyDetectionResponse],
)
def fetch_all_anomalies(
    db: Session = Depends(get_db),
):

    return get_all_anomalies(db)



# ==========================================
# Get Employee Anomalies
# ==========================================

@router.get(
    "/employee/{employee_id}",
    response_model=List[AnomalyDetectionResponse],
)
def fetch_employee_anomalies(
    employee_id: int,
    db: Session = Depends(get_db),
):

    return get_employee_anomalies(
        db,
        employee_id,
    )