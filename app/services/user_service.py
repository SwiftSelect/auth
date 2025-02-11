from sqlalchemy.orm import Session
from app.models.users import User
from app.models.roles import Role
from app.models.roles_actions_map import RoleActionMap
from app.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.dto.user_signup import UserSignup
from app.dto.user_login import UserLogin, UserLoginResponse
from app.dto.token_claims import TokenClaims
from fastapi import HTTPException

def register_user(db: Session, user: UserSignup):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        return None
    
    hashed_pw = hash_password(user.password)
    new_user = User(username=user.email, password=hashed_pw, role=user.role, firstname=user.firstname, lastname=user.lastname)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(db: Session, user: UserLogin):
    user = db.query(User).filter(User.email == user.email).first()
    if not user or not verify_password(user.password, user.password):
        return None
    claims = TokenClaims(email=user.email, role=user.role, fullname=user.firstname+" "+user.lastname)
    access_token = create_access_token(claims)
    refresh_token = create_refresh_token(claims)
    return UserLoginResponse(access_token, refresh_token)

def validate_token(db: Session, token:str, action: str):
    user = get_user(db, token)
    role = db.query(Role).get(user.role)
    role_action = db.query(RoleActionMap).filter(role_id=role.id, action_name=action)
    if not role_action:
        raise HTTPException(status_code=403, detail="Forbidden")
    return True

def get_user(db: Session, token: str):
    tc: TokenClaims = decode_token(token)
    if not tc:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(User).filter(User.email == tc.email).first()
    if not user or not verify_password(user.password, user.password):
        raise HTTPException(status_code=401, detail="Unauthorized") 
    return user