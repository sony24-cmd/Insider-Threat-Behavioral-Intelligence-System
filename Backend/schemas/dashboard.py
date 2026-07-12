from pydantic import BaseModel
from typing import List


class DashboardSummary(BaseModel):
    total_users: int
    total_employees: int
    total_devices: int
    total_activity_logs: int
    total_risk_scores: int
    total_alerts: int
    critical_alerts: int
    total_notifications: int


class AlertSeverity(BaseModel):
    severity: str
    count: int


class DepartmentSummary(BaseModel):
    department: str
    total_employees: int


class HighRiskEmployee(BaseModel):
    employee_id: str
    department: str
    risk_score: float


class RecentActivity(BaseModel):
    employee_id: int
    activity_type: str
    timestamp: str