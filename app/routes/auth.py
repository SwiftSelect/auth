from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.user_service import register_user, authenticate_user, validate_token, get_user
from app.dto.user_signup import  UserSignup 
from app.dto.user_login import UserLogin, UserLoginResponse, UserResponse
from app.dto.validate import ValidateUser
from typing import Optional

router = APIRouter()

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: UserSignup, db: Session = Depends(get_db)):
    new_user = register_user(db, user)
    if not new_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    return {"message": "User created successfully"}

@router.post("/login", response_model=UserLoginResponse)
def login(form_data: UserLogin, db: Session = Depends(get_db)):
    tokens = authenticate_user(db, form_data)
    if not tokens:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return tokens

@router.post("/validate", response_model=UserLoginResponse)
def validate(data: ValidateUser, db: Session = Depends(get_db)):
    return validate_token(db, data.token, data.action)

@router.get("/get_user", response_model=UserResponse)
def user(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    token = authorization.split("Bearer ")[1]
    return get_user(db, token)