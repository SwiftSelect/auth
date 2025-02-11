from fastapi import FastAPI
from app.routes import auth
from app.database import init_db

app = FastAPI(title="Authorization Service with Role-Based Access Control")

# Create tables on startup
init_db()

# Include API routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
# app.include_router(role.router, prefix="/roles", tags=["Roles"])
# app.include_router(action.router, prefix="/actions", tags=["Actions"])
