from sqlalchemy.orm import Session
from sqlalchemy import func

from models.employee import Employee
from models.device import Device
from models.activity_log import ActivityLog
from models.alert import Alert
from models.notification import Notification
from models.risk_score import RiskScore


# ==========================================
# Dashboard Summary
# ==========================================

def get_dashboard_summary(db: Session):

    return {
        "total_employees": db.query(Employee).count(),
        "total_devices": db.query(Device).count(),
        "total_activity_logs": db.query(ActivityLog).count(),
        "total_alerts": db.query(Alert).count(),
        "total_notifications": db.query(Notification).count(),
        "high_risk_employees": db.query(RiskScore).filter(
            RiskScore.risk_level.in_(["High", "Critical"])
        ).count(),
    }


# ==========================================
# Alert Severity Summary
# ==========================================

def get_alert_severity(db: Session):

    results = (
        db.query(
            Alert.severity,
            func.count(Alert.id)
        )
        .group_by(Alert.severity)
        .all()
    )

    return [
        {
            "severity": severity,
            "count": count,
        }
        for severity, count in results
    ]


# ==========================================
# Department Summary
# ==========================================

def get_department_summary(db: Session):

    results = (
        db.query(
            Employee.department,
            func.count(Employee.id)
        )
        .group_by(Employee.department)
        .all()
    )

    return [
        {
            "department": department,
            "employees": count,
        }
        for department, count in results
    ]


# ==========================================
# High Risk Employees
# ==========================================

def get_high_risk_employees(db: Session):

    results = (
        db.query(RiskScore)
        .filter(
            RiskScore.risk_level.in_(["High", "Critical"])
        )
        .order_by(RiskScore.risk_score.desc())
        .limit(10)
        .all()
    )

    return results


# ==========================================
# Recent Activities
# ==========================================

def get_recent_activities(db: Session):

    return (
        db.query(ActivityLog)
        .order_by(ActivityLog.timestamp.desc())
        .limit(10)
        .all()
    )


# ==========================================
# Top Alerts
# ==========================================

def get_top_alerts(db: Session):

    return (
        db.query(Alert)
        .order_by(Alert.created_at.desc())
        .limit(10)
        .all()
    )