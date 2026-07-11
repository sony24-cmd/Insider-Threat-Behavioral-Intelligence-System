from sqlalchemy.orm import Session

from models.alert import Alert
from schemas.alert import AlertCreate, AlertUpdate


# ==========================================
# Create Alert
# ==========================================

def create_alert(
    db: Session,
    alert: AlertCreate
):
    new_alert = Alert(**alert.model_dump())

    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)

    return new_alert


# ==========================================
# Get All Alerts
# ==========================================

def get_all_alerts(db: Session):
    return db.query(Alert).all()


# ==========================================
# Get Alert by ID
# ==========================================

def get_alert(
    db: Session,
    alert_id: int
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
    alert: AlertUpdate
):
    existing_alert = (
        db.query(Alert)
        .filter(Alert.id == alert_id)
        .first()
    )

    if not existing_alert:
        return None

    update_data = alert.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(existing_alert, key, value)

    db.commit()
    db.refresh(existing_alert)

    return existing_alert


# ==========================================
# Delete Alert
# ==========================================

def delete_alert(
    db: Session,
    alert_id: int
):
    existing_alert = (
        db.query(Alert)
        .filter(Alert.id == alert_id)
        .first()
    )

    if not existing_alert:
        return None

    db.delete(existing_alert)
    db.commit()

    return existing_alert