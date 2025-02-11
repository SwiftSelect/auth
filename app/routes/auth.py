from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.user_service import register_user, authenticate_user, validate_token, get_user
from app.dto.user_signup import  UserSignup 
from app.dto.user_login import UserLogin, UserLoginResponse
from app.dto.validate import ValidateUser

router = APIRouter()

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: UserSignup, db: Session = Depends(get_db)):
    new_user = register_user(db, user)
    if not new_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    return {"message": "User created successfully"}

@router.post("/login", response_model=UserLoginResponse)
def login(form_data: UserLogin, db: Session = Depends(get_db)):
    tokens = authenticate_user(db, form_data.username, form_data.password)
    if not tokens:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return tokens

@router.post("/validate", response_model=UserLoginResponse)
def validate(data: ValidateUser, db: Session = Depends(get_db)):
    return validate_token(db, data.token, data.action)

@router.post("/get_user", response_model=UserLoginResponse)
def user(token: str, db: Session = Depends(get_db)):
    return get_user(db, token)