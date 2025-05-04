from sqlalchemy.orm import Session
from app.models.users import User
from app.models.roles import Role
from app.models.orgs import Org
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
    org_id = None
    if user.role in [1, 2]:  # Only ADMIN(1) and RECRUITER(2) need org check
        org = db.query(Org).filter(Org.domain == user.email.split("@")[1]).first()
        if not org:
            raise HTTPException(status_code = 404, detail="Organization not registered")
        org_id = org.id
    new_user = User(email=user.email, password=hashed_pw, role_id=user.role, firstname=user.firstName, lastname=user.lastName, org_id=org_id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(db: Session, user: UserLogin):
    c_u = db.query(User).filter(User.email == user.email).first()
    if not c_u or not verify_password(user.password, c_u.password):
        return None
    claims = TokenClaims(id=c_u.id, email=c_u.email, role=c_u.role.name, firstname=c_u.firstname, lastname=c_u.lastname)
    access_token = create_access_token(claims)
    refresh_token = create_refresh_token(claims)
    return UserLoginResponse(access_token=access_token, refresh_token=refresh_token)

def validate_token(db: Session, token:str, action: str):
    user = get_user(db, token)
    role = db.query(Role).filter(Role.id == user.role_id).first()
    if not role:
        raise HTTPException(status_code=403, detail="Role not found")
        
    # Check if the role has permission for the action
    role_action = db.query(RoleActionMap).filter(
        RoleActionMap.role_id == role.id, 
        RoleActionMap.action_name == action
    ).first()
    
    if not role_action:
        raise HTTPException(status_code=403, detail="Forbidden")
        
    # Return user information in the response
    access_token = create_access_token({"email": user.email, "role": role.name})
    refresh_token = create_refresh_token({"email": user.email, "role": role.name})
    return UserLoginResponse(access_token=access_token, refresh_token=refresh_token)

def get_user(db: Session, token: str) -> User:
    decoded_token = decode_token(token)
    if not decoded_token:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    # Create a TokenClaims object from the decoded token
    try:
        user = db.query(User).filter(User.email == decoded_token['email']).first()
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized")
        print(f"user: {user}")
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token format: {str(e)}")
    
def get_org_details(db: Session, org_id: int):
    org = db.query(Org).filter(Org.id == org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org