from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas.notification import (
    NotificationCreate,
    NotificationResponse,
)
from services.notification_service import (
    create_notification,
    get_notifications,
    get_notification_by_id,
    delete_notification,
)

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


@router.post("/", response_model=NotificationResponse)
def add_notification(
    notification: NotificationCreate,
    db: Session = Depends(get_db),
):
    return create_notification(db, notification)


@router.get("/", response_model=List[NotificationResponse])
def fetch_notifications(
    db: Session = Depends(get_db),
):
    return get_notifications(db)


@router.get("/{notification_id}", response_model=NotificationResponse)
def fetch_notification(
    notification_id: int,
    db: Session = Depends(get_db),
):
    notification = get_notification_by_id(db, notification_id)

    if not notification:
        raise HTTPException(
            status_code=404,
            detail="Notification not found",
        )

    return notification


@router.delete("/{notification_id}")
def remove_notification(
    notification_id: int,
    db: Session = Depends(get_db),
):
    notification = delete_notification(db, notification_id)

    if not notification:
        raise HTTPException(
            status_code=404,
            detail="Notification not found",
        )

    return {"message": "Notification deleted successfully"}