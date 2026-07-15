from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db

from services.dashboard_service import (
    get_dashboard_summary,
    get_alert_severity,
    get_department_summary,
    get_high_risk_employees,
    get_recent_activities,
    get_top_alerts,
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


# ==========================================
# Dashboard Summary
# ==========================================

@router.get("/summary")
def dashboard_summary(db: Session = Depends(get_db)):
    return get_dashboard_summary(db)


# ==========================================
# Alert Severity Summary
# ==========================================

@router.get("/alert-severity")
def alert_severity(db: Session = Depends(get_db)):
    return get_alert_severity(db)


# ==========================================
# Department Summary
# ==========================================

@router.get("/department-summary")
def department_summary(db: Session = Depends(get_db)):
    return get_department_summary(db)


# ==========================================
# High Risk Employees
# ==========================================

@router.get("/high-risk-employees")
def high_risk_employees(db: Session = Depends(get_db)):
    return get_high_risk_employees(db)


# ==========================================
# Recent Activities
# ==========================================

@router.get("/recent-activities")
def recent_activities(db: Session = Depends(get_db)):
    return get_recent_activities(db)


# ==========================================
# Top Alerts
# ==========================================

@router.get("/top-alerts")
def top_alerts(db: Session = Depends(get_db)):
    return get_top_alerts(db)