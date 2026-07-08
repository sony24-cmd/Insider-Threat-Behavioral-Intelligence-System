from fastapi import FastAPI

from database import Base, engine

from routes.auth import router as auth_router
from routes.users import router as users_router
from routes.admin import router as admin_router


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="AI Insider Threat Behavioral Intelligence System",
    version="1.0.0",
)


# Include routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(admin_router)


@app.get("/")
def root():
    return {
        "message": "AI Insider Threat Behavioral Intelligence System API is running"
    }