from sqlalchemy.orm import Session

from models.notification import Notification

from schemas.notification import (
    NotificationCreate,
    NotificationUpdate,
)


# ==========================================
# Create Notification
# ==========================================

def create_notification(
    db: Session,
    notification: NotificationCreate,
):

    db_notification = Notification(
        title=notification.title,
        message=notification.message,
        notification_type=notification.notification_type,
        status=notification.status,
    )

    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)

    return db_notification


# ==========================================
# Get All Notifications
# ==========================================

def get_all_notifications(db: Session):

    return (
        db.query(Notification)
        .order_by(Notification.created_at.desc())
        .all()
    )


# ==========================================
# Get Notification By ID
# ==========================================

def get_notification(
    db: Session,
    notification_id: int,
):

    return (
        db.query(Notification)
        .filter(Notification.id == notification_id)
        .first()
    )


# ==========================================
# Update Notification
# ==========================================

def update_notification(
    db: Session,
    notification_id: int,
    notification: NotificationUpdate,
):

    db_notification = (
        db.query(Notification)
        .filter(Notification.id == notification_id)
        .first()
    )

    if not db_notification:
        return None

    for key, value in notification.model_dump(
        exclude_unset=True
    ).items():
        setattr(db_notification, key, value)

    db.commit()
    db.refresh(db_notification)

    return db_notification


# ==========================================
# Mark Notification As Read
# ==========================================

def mark_as_read(
    db: Session,
    notification_id: int,
):

    notification = (
        db.query(Notification)
        .filter(Notification.id == notification_id)
        .first()
    )

    if not notification:
        return None

    notification.status = "Read"

    db.commit()
    db.refresh(notification)

    return notification


# ==========================================
# Delete Notification
# ==========================================

def delete_notification(
    db: Session,
    notification_id: int,
):

    notification = (
        db.query(Notification)
        .filter(Notification.id == notification_id)
        .first()
    )

    if not notification:
        return None

    db.delete(notification)
    db.commit()

    return notification