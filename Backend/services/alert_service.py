from sqlalchemy.orm import Session

from models.alert import Alert
from models.notification import Notification

from schemas.alert import (
    AlertCreate,
    AlertUpdate,
)


# ==========================================
# Create Alert
# ==========================================

def create_alert(
    db: Session,
    employee_id: int,
    risk_score_id: int,
    severity: str,
    description: str,
):

    alert = Alert(
        employee_id=employee_id,
        risk_score_id=risk_score_id,
        severity=severity,
        description=description,
        status="Open",
    )

    db.add(alert)
    db.commit()
    db.refresh(alert)

    # ======================================
    # Auto Notification
    # ======================================

    if severity in ["High", "Critical"]:

        notification = Notification(
            title=f"{severity} Risk Alert",
            message=description,
            notification_type="Alert",
            status="Unread",
        )

        db.add(notification)
        db.commit()

    return alert


# ==========================================
# Manual Create Alert
# ==========================================

def create_manual_alert(
    db: Session,
    alert_data: AlertCreate,
):

    alert = Alert(**alert_data.model_dump())

    db.add(alert)
    db.commit()
    db.refresh(alert)

    return alert


# ==========================================
# Get All Alerts
# ==========================================

def get_all_alerts(db: Session):

    return db.query(Alert).all()


# ==========================================
# Get Alert
# ==========================================

def get_alert(
    db: Session,
    alert_id: int,
):

    return (
        db.query(Alert)
        .filter(Alert.id == alert_id)
        .first()
    )


# ==========================================
# Update Alert
# ==========================================

def update_alert(
    db: Session,
    alert_id: int,
    alert_update: AlertUpdate,
):

    alert = (
        db.query(Alert)
        .filter(Alert.id == alert_id)
        .first()
    )

    if not alert:
        return None

    for key, value in alert_update.model_dump(
        exclude_unset=True
    ).items():
        setattr(alert, key, value)

    db.commit()
    db.refresh(alert)

    return alert


# ==========================================
# Delete Alert
# ==========================================

def delete_alert(
    db: Session,
    alert_id: int,
):

    alert = (
        db.query(Alert)
        .filter(Alert.id == alert_id)
        .first()
    )

    if not alert:
        return None

    db.delete(alert)
    db.commit()

    return alert