from sqlalchemy.orm import Session

from models.activity_log import ActivityLog
from schemas.activity_log import ActivityLogCreate

from services.ai_service import predict_risk
from services.risk_score_service import save_ai_risk_score
from services.alert_service import create_alert

# Behavior Profile Service
from services.behavior_analysis_service import (
    generate_behavior_profile,
)

# NEW: Feature Extraction Service
from services.anomaly_detection_service import (
    extract_employee_features,
)


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
    # Update Employee Behavior Profile
    # --------------------------------------

    generate_behavior_profile(
        db=db,
        employee_id=activity.employee_id,
    )

    # --------------------------------------
    # Extract Real Employee Features
    # --------------------------------------

    features = extract_employee_features(
        db=db,
        employee_id=activity.employee_id,
    )

    # --------------------------------------
    # AI Risk Prediction
    # --------------------------------------

    prediction = predict_risk(
        login_count=features["login_count"],
        logout_count=features["logout_count"],
        usb_connect=features["usb_connect"],
        usb_disconnect=features["usb_disconnect"],
        http_visits=features["http_visits"],
        total_events=features["total_events"],
    )

    # --------------------------------------
    # Save AI Risk Score
    # --------------------------------------

    risk = save_ai_risk_score(
        db=db,
        employee_id=activity.employee_id,
        confidence=prediction["confidence"],
    )

    # --------------------------------------
    # Auto Create Alert
    # --------------------------------------

    if prediction["risk_level"] in ["High", "Critical"]:

        create_alert(
            db=db,
            employee_id=activity.employee_id,
            risk_score_id=risk.id,
            severity=prediction["risk_level"],
            description="AI detected suspicious insider behaviour.",
        )

    return db_activity