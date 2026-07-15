from sqlalchemy.orm import Session

from models.activity_log import ActivityLog
from schemas.activity_log import ActivityLogCreate

from services.ai_service import predict_risk
from services.risk_score_service import save_ai_risk_score
from services.alert_service import create_alert


def create_activity_log(db: Session, activity: ActivityLogCreate):

    # Save Activity Log
    db_activity = ActivityLog(
        employee_id=activity.employee_id,
        activity_type=activity.activity_type,
        description=activity.description,
        ip_address=activity.ip_address,
        device_name=activity.device_name,
        risk_level=activity.risk_level,
    )

    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)

    # --------------------------------------
    # Temporary feature values
    # Replace these later with real values
    # --------------------------------------

    prediction = predict_risk(
        login_count=10,
        logout_count=9,
        usb_connect=1,
        usb_disconnect=1,
        http_visits=35,
        total_events=56,
    )

    # Save Risk Score
    risk = save_ai_risk_score(
        db,
        employee_id=activity.employee_id,
        confidence=prediction["confidence"],
    )

    # Auto Alert
    if prediction["risk_level"] in ["High", "Critical"]:
        create_alert(
            db=db,
            employee_id=activity.employee_id,
            risk_score_id=risk.id,
            severity=prediction["risk_level"],
            description="AI detected suspicious insider behaviour.",
        )

    return db_activity