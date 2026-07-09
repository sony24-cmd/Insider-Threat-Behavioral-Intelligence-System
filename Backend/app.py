from fastapi import FastAPI

from database import Base, engine

# Import Models (Required so SQLAlchemy creates all tables)
from models.user import User
from models.employee import Employee
from models.device import Device

# Import Routers
from routes.auth import router as auth_router
from routes.users import router as users_router
from routes.admin import router as admin_router
from routes.employee import router as employee_router
from routes.device import router as device_router

# Create all database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI Application
app = FastAPI(
    title="AI Insider Threat Behavioral Intelligence System",
    version="1.0.0",
    description="Backend API for AI-powered Insider Threat Behavioral Intelligence System",
)

# Register API Routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(admin_router)
app.include_router(employee_router)
app.include_router(device_router)

# Root Endpoint
@app.get("/", tags=["Home"])
def root():
    return {
        "status": "success",
        "message": "AI Insider Threat Behavioral Intelligence System API is running",
        "version": "1.0.0",
    }