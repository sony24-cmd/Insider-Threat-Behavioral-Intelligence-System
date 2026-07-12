from fastapi import FastAPI

from database import Base, engine

# ==========================================
# Import Models (Required for SQLAlchemy)
# ==========================================
from models.user import User
from models.employee import Employee
from models.device import Device
from models.access_privilege import AccessPrivilege
from models.activity_log import ActivityLog
from models.risk_score import RiskScore
from models.alert import Alert
from models.notification import Notification

# ==========================================
# Import Routers
# ==========================================
from routes.auth import router as auth_router
from routes.users import router as users_router
from routes.admin import router as admin_router
from routes.employee import router as employee_router
from routes.device import router as device_router
from routes.access_privilege import router as access_router
from routes.activity_log import router as activity_log_router
from routes.risk_score import router as risk_score_router
from routes.alert import router as alert_router
from routes.notification_routes import router as notification_router
from routes.dashboard import router as dashboard_router

# ========= NEW AI ROUTER =========
from routes.ai import router as ai_router

# ==========================================
# Create Database Tables
# ==========================================
Base.metadata.create_all(bind=engine)

# ==========================================
# Initialize FastAPI
# ==========================================
app = FastAPI(
    title="AI Insider Threat Behavioral Intelligence System",
    version="1.0.0",
    description="Backend API for AI-powered Insider Threat Behavioral Intelligence System",
)

# ==========================================
# Register Routers
# ==========================================
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(admin_router)
app.include_router(employee_router)
app.include_router(device_router)
app.include_router(access_router)
app.include_router(activity_log_router)
app.include_router(risk_score_router)
app.include_router(alert_router)
app.include_router(notification_router)
app.include_router(dashboard_router)

# ========= REGISTER AI ROUTER =========
app.include_router(ai_router)

# ==========================================
# Root Endpoint
# ==========================================
@app.get("/", tags=["Home"])
def root():
    return {
        "status": "success",
        "message": "AI Insider Threat Behavioral Intelligence System API is running",
        "version": "1.0.0",
    }