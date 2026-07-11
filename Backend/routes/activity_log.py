from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas.activity_log import (
    ActivityLogCreate,
    ActivityLogResponse,
    ActivityLogUpdate,
)
from services import activity_log_service

router = APIRouter(
    prefix="/activity-logs",
    tags=["Activity Logs"],
)


# -----------------------------
# Create Activity Log
# -----------------------------
@router.post("/", response_model=ActivityLogResponse)
def create_activity_log(
    activity: ActivityLogCreate,
    db: Session = Depends(get_db),
):
    return activity_log_service.create_activity_log(db, activity)


# -----------------------------
# Get All Activity Logs
# -----------------------------
@router.get("/", response_model=list[ActivityLogResponse])
def get_all_activity_logs(
    db: Session = Depends(get_db),
):
    return activity_log_service.get_all_activity_logs(db)


# -----------------------------
# Get Activity Log by ID
# -----------------------------
@router.get("/{activity_id}", response_model=ActivityLogResponse)
def get_activity_log(
    activity_id: int,
    db: Session = Depends(get_db),
):
    activity = activity_log_service.get_activity_log(
        db,
        activity_id,
    )

    if activity is None:
        raise HTTPException(
            status_code=404,
            detail="Activity Log not found",
        )

    return activity


# -----------------------------
# Update Activity Log
# -----------------------------
@router.put("/{activity_id}", response_model=ActivityLogResponse)
def update_activity_log(
    activity_id: int,
    activity: ActivityLogUpdate,
    db: Session = Depends(get_db),
):
    updated = activity_log_service.update_activity_log(
        db,
        activity_id,
        activity,
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Activity Log not found",
        )

    return updated


# -----------------------------
# Delete Activity Log
# -----------------------------
@router.delete("/{activity_id}")
def delete_activity_log(
    activity_id: int,
    db: Session = Depends(get_db),
):
    deleted = activity_log_service.delete_activity_log(
        db,
        activity_id,
    )

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Activity Log not found",
        )

    return {
        "message": "Activity Log deleted successfully"
    }