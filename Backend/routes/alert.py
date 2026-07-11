from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db

from schemas.alert import (
    AlertCreate,
    AlertResponse,
    AlertUpdate,
)

from services import alert_service


router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)


# ==========================================
# Create Alert
# ==========================================

@router.post("/", response_model=AlertResponse)
def create_alert(
    alert: AlertCreate,
    db: Session = Depends(get_db)
):
    return alert_service.create_alert(db, alert)


# ==========================================
# Get All Alerts
# ==========================================

@router.get("/", response_model=list[AlertResponse])
def get_all_alerts(
    db: Session = Depends(get_db)
):
    return alert_service.get_all_alerts(db)


# ==========================================
# Get Alert By ID
# ==========================================

@router.get("/{alert_id}", response_model=AlertResponse)
def get_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):
    alert = alert_service.get_alert(
        db,
        alert_id,
    )

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found",
        )

    return alert


# ==========================================
# Update Alert
# ==========================================

@router.put("/{alert_id}", response_model=AlertResponse)
def update_alert(
    alert_id: int,
    alert: AlertUpdate,
    db: Session = Depends(get_db)
):
    updated = alert_service.update_alert(
        db,
        alert_id,
        alert,
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found",
        )

    return updated


# ==========================================
# Delete Alert
# ==========================================

@router.delete("/{alert_id}")
def delete_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):
    deleted = alert_service.delete_alert(
        db,
        alert_id,
    )

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found",
        )

    return {
        "message": "Alert deleted successfully"
    }