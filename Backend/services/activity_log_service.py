from datetime import datetime

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

# Feature Extraction Service
from services.anomaly_detection_service import (
    extract_employee_features,
)

# Behavior Profile
from services.behavior_profile_service import (
    get_behavior_profile_by_employee,
)

# Anomaly Rule Engine
from services.anomaly_rule_engine import (
    detect_login_anomaly,
    detect_after_hours,
    detect_weekend_activity,
    detect_usb_anomaly,
    detect_network_anomaly,
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
    # Update Behavior Profile
    # --------------------------------------

    generate_behavior_profile(
        db=db,
        employee_id=activity.employee_id,
    )

    # --------------------------------------
    # Extract Employee Features
    # --------------------------------------

    features = extract_employee_features(
        db=db,
        employee_id=activity.employee_id,
    )

    # --------------------------------------
    # Load Employee Behavior Profile
    # --------------------------------------

    profile = get_behavior_profile_by_employee(
        db=db,
        employee_id=activity.employee_id,
    )

    anomalies = []

   if profile:

    login_result = detect_login_anomaly(
        profile,
        datetime.utcnow(),
    )

    if login_result["anomaly"]:
        anomalies.append(login_result)

    after_hours = detect_after_hours(
        datetime.utcnow(),
    )

    if after_hours["anomaly"]:
        anomalies.append(after_hours)

    weekend = detect_weekend_activity(
        datetime.utcnow(),
    )

    if weekend["anomaly"]:
        anomalies.append(weekend)

    usb = detect_usb_anomaly(
        features["usb_connect"],
    )

    if usb["anomaly"]:
        anomalies.append(usb)

    network = detect_network_anomaly(
        features["http_visits"],
    )

    if network["anomaly"]:
        anomalies.append(network)

# --------------------------------------
# Save Detected Anomalies
# --------------------------------------

for anomaly in anomalies:

    save_anomaly(
        db=db,
        employee_id=activity.employee_id,
        anomaly_score=anomaly["score"],
        anomaly_level=anomaly["level"],
        reason=anomaly["reason"],
    )

    # --------------------------------------
    # AI Prediction
    # --------------------------------------

    prediction = predict_risk(
    login_count=features["login_count"],
    logout_count=features["logout_count"],
    usb_connect=features["usb_connect"],
    usb_disconnect=features["usb_disconnect"],
    http_visits=features["http_visits"],
    suspicious_http_visits=features["suspicious_http_visits"],
    after_hours_events=features["after_hours_events"],
    unique_devices=features["unique_devices"],
    total_events=features["total_events"],
)

    # --------------------------------------
    # Update Risk Level using Anomalies
    # --------------------------------------

    if len(anomalies) >= 3:
        prediction["risk_level"] = "Critical"

    elif len(anomalies) == 2:
        prediction["risk_level"] = "High"

    elif len(anomalies) == 1:
        prediction["risk_level"] = "Medium"

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

        alert_message = (
            "\n".join(
                anomaly["reason"]
                for anomaly in anomalies
            )
            if anomalies
            else "AI detected suspicious insider behaviour."
        )

        create_alert(
            db=db,
            employee_id=activity.employee_id,
            risk_score_id=risk.id,
            severity=prediction["risk_level"],
            description=alert_message,
        )

    return db_activity