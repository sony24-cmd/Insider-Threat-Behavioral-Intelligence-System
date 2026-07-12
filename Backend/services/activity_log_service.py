from sqlalchemy.orm import Session

from models.activity_log import ActivityLog
from schemas.activity_log import (
    ActivityLogCreate,
    ActivityLogUpdate,
)

# AI Service
from services.ai_service import predict_risk

# Risk Score Service
from services.risk_score_service import save_ai_risk_score

# Alert Service
from services.alert_service import create_alert

# Alert Schema
from schemas.alert import AlertCreate


# ==========================================
# Create Activity Log
# ==========================================
def create_activity_log(
    db: Session,
    activity: ActivityLogCreate,
):
    # --------------------------------------
    # Save Activity Log
    # --------------------------------------

    db_activity = ActivityLog(**activity.model_dump())

    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)

    # --------------------------------------
    # Temporary AI Features
    # (Later these will come from
    # employee activity aggregation)
    # --------------------------------------

    login_count = 1
    logout_count = 1

    usb_connect = 1
    usb_disconnect = 0

    http_visits = 1

    suspicious_http_visits = 1

    after_hours_events = 1

    unique_devices = 1

    total_events = (
        login_count
        + logout_count
        + usb_connect
        + usb_disconnect
        + http_visits
    )

    # --------------------------------------
    # AI Prediction
    # --------------------------------------

    ai_result = predict_risk(
        login_count=login_count,
        logout_count=logout_count,
        usb_connect=usb_connect,
        usb_disconnect=usb_disconnect,
        http_visits=http_visits,
        suspicious_http_visits=suspicious_http_visits,
        after_hours_events=after_hours_events,
        unique_devices=unique_devices,
        total_events=total_events,
    )

    # --------------------------------------
    # Save AI Risk Score
    # --------------------------------------

    risk = save_ai_risk_score(
        db=db,
        employee_id=db_activity.employee_id,
        confidence=ai_result["confidence"],
    )

    # --------------------------------------
    # Generate Alert
    # --------------------------------------

    if risk.risk_level in ["High", "Medium"]:

        alert = AlertCreate(
            employee_id=db_activity.employee_id,
            risk_score_id=risk.id,
            alert_type="AI Insider Threat",
            severity=risk.risk_level,
            description=f"AI detected {risk.risk_level} risk behaviour.",
            status="Open",
        )

        create_alert(
            db=db,
            alert=alert,
        )

    return db_activity


# ==========================================
# Get Activity Log By ID
# ==========================================
def get_activity_log(
    db: Session,
    activity_id: int,
):
    return (
        db.query(ActivityLog)
        .filter(ActivityLog.id == activity_id)
        .first()
    )


# ==========================================
# Get All Activity Logs
# ==========================================
def get_all_activity_logs(
    db: Session,
):
    return db.query(ActivityLog).all()


# ==========================================
# Update Activity Log
# ==========================================
def update_activity_log(
    db: Session,
    activity_id: int,
    activity: ActivityLogUpdate,
):
    db_activity = (
        db.query(ActivityLog)
        .filter(ActivityLog.id == activity_id)
        .first()
    )

    if not db_activity:
        return None

    update_data = activity.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(
            db_activity,
            key,
            value,
        )

    db.commit()
    db.refresh(db_activity)

    return db_activity


# ==========================================
# Delete Activity Log
# ==========================================
def delete_activity_log(
    db: Session,
    activity_id: int,
):
    db_activity = (
        db.query(ActivityLog)
        .filter(ActivityLog.id == activity_id)
        .first()
    )

    if not db_activity:
        return None

    db.delete(db_activity)
    db.commit()

    return db_activity