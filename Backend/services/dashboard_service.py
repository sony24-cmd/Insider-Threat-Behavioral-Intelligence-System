from sqlalchemy.orm import Session
from sqlalchemy import func

from models.user import User
from models.employee import Employee
from models.device import Device
from models.activity_log import ActivityLog
from models.risk_score import RiskScore
from models.alert import Alert
from models.notification import Notification


# ==========================================================
# Dashboard Summary
# ==========================================================

def get_dashboard_summary(db: Session):
    return {
        "total_users": db.query(func.count(User.id)).scalar(),
        "total_employees": db.query(func.count(Employee.id)).scalar(),
        "total_devices": db.query(func.count(Device.id)).scalar(),
        "total_activity_logs": db.query(func.count(ActivityLog.id)).scalar(),
        "total_risk_scores": db.query(func.count(RiskScore.id)).scalar(),
        "total_alerts": db.query(func.count(Alert.id)).scalar(),
        "critical_alerts": db.query(Alert).filter(
            Alert.severity == "Critical"
        ).count(),
        "total_notifications": db.query(func.count(Notification.id)).scalar(),
    }


# ==========================================================
# Alert Severity Analytics
# ==========================================================

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
            "count": count
        }
        for severity, count in results
    ]


# ==========================================================
# Department Summary
# ==========================================================

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
            "total_employees": total
        }
        for department, total in results
    ]


# ==========================================================
# High Risk Employees
# ==========================================================

def get_high_risk_employees(db: Session):

    results = (
        db.query(
            Employee.employee_id,
            Employee.department,
            RiskScore.risk_score
        )
        .join(
            RiskScore,
            Employee.id == RiskScore.employee_id
        )
        .order_by(
            RiskScore.risk_score.desc()
        )
        .limit(5)
        .all()
    )

    return [
        {
            "employee_id": emp_id,
            "department": department,
            "risk_score": risk_score
        }
        for emp_id, department, risk_score in results
    ]


# ==========================================================
# Recent Activities
# ==========================================================

def get_recent_activities(db: Session):

    activities = (
        db.query(ActivityLog)
        .order_by(
            ActivityLog.created_at.desc()
        )
        .limit(10)
        .all()
    )

    return activities


# ==========================================================
# Dashboard Cards (Optional)
# ==========================================================

def get_dashboard_cards(db: Session):

    return {
        "employees": db.query(Employee).count(),
        "devices": db.query(Device).count(),
        "activities": db.query(ActivityLog).count(),
        "risk_scores": db.query(RiskScore).count(),
        "alerts": db.query(Alert).count(),
        "notifications": db.query(Notification).count()
    }


# ==========================================================
# Top Alert Types
# ==========================================================

def get_top_alert_types(db: Session):

    results = (
        db.query(
            Alert.alert_type,
            func.count(Alert.id)
        )
        .group_by(Alert.alert_type)
        .order_by(
            func.count(Alert.id).desc()
        )
        .limit(5)
        .all()
    )

    return [
        {
            "alert_type": alert_type,
            "count": count
        }
        for alert_type, count in results
    ]


# ==========================================================
# Open vs Closed Alerts
# ==========================================================

def get_alert_status(db: Session):

    results = (
        db.query(
            Alert.status,
            func.count(Alert.id)
        )
        .group_by(Alert.status)
        .all()
    )

    return [
        {
            "status": status,
            "count": count
        }
        for status, count in results
    ]