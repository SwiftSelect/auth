from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth
from app.database import init_db

app = FastAPI(title="Authorization Service with Role-Based Access Control")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],  # Frontend URL, jobs-svc
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

init_db()

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
# app.include_router(role.router, prefix="/roles", tags=["Roles"])
# app.include_router(action.router, prefix="/actions", tags=["Actions"])
