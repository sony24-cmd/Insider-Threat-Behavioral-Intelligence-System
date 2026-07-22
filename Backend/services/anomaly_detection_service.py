from sqlalchemy.orm import Session

from models.anomaly_detection import AnomalyDetection


# ==========================================
# Get All Anomalies
# ==========================================

def get_all_anomalies(
    db: Session
):

    return (
        db.query(AnomalyDetection)
        .all()
    )


# ==========================================
# Get Employee Anomalies
# ==========================================

def get_employee_anomalies(
    db: Session,
    employee_id: int,
):

    return (
        db.query(AnomalyDetection)
        .filter(
            AnomalyDetection.employee_id == employee_id
        )
        .all()
    )


# ==========================================
# Save Anomaly
# ==========================================

def save_anomaly(
    db: Session,
    employee_id: int,
    anomaly_score: float,
    anomaly_level: str,
    reason: str,
):

    anomaly = AnomalyDetection(

        employee_id=employee_id,

        anomaly_score=anomaly_score,

        anomaly_level=anomaly_level,

        reason=reason,

    )


    db.add(anomaly)
    db.commit()
    db.refresh(anomaly)

    return anomaly



# ==========================================
# Feature Extraction
# ==========================================

def extract_employee_features(
    db: Session,
    employee_id: int,
):

    # Temporary feature extraction
    # Later we connect CERT dataset features

    return {

        "login_count": 0,

        "logout_count": 0,

        "usb_connect": 0,

        "usb_disconnect": 0,

        "http_visits": 0,

        "suspicious_http_visits": 0,

        "after_hours_events": 0,

        "unique_devices": 0,

        "total_events": 0,

    }