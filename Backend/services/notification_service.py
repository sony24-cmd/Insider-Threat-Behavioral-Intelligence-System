from sqlalchemy.orm import Session

from models.notification import Notification
from schemas.notification import NotificationCreate


# ==========================================
# Create Notification
# ==========================================

def create_notification(
    db: Session,
    notification: NotificationCreate
):
    new_notification = Notification(
        **notification.model_dump()
    )

    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)

    return new_notification


# ==========================================
# Auto Create Notification from Alert
# ==========================================

def create_notification_from_alert(
    db: Session,
    alert
):
    notification = Notification(
        title="Security Alert",
        message=(
            f"{alert.alert_type} detected for "
            f"Employee ID {alert.employee_id}. "
            f"{alert.description}"
        ),
        severity=alert.severity,
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    return notification


# ==========================================
# Get All Notifications
# ==========================================

def get_notifications(db: Session):
    return db.query(Notification).all()


# ==========================================
# Get Notification By ID
# ==========================================

def get_notification_by_id(
    db: Session,
    notification_id: int
):
    return (
        db.query(Notification)
        .filter(Notification.id == notification_id)
        .first()
    )


# ==========================================
# Delete Notification
# ==========================================

def delete_notification(
    db: Session,
    notification_id: int
):
    notification = (
        db.query(Notification)
        .filter(Notification.id == notification_id)
        .first()
    )

    if notification:
        db.delete(notification)
        db.commit()

    return notification