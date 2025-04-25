from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.dto.token_claims import TokenClaims
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return create_token(data, expire)

def create_refresh_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    return create_token(data, expire)

def create_token(data: dict, expire: datetime):
    # Handle Pydantic models by converting to dict
    if hasattr(data, "dict"):
        # This is a Pydantic model
        to_encode = data.dict()
    elif hasattr(data, "__dict__"):
        # This is a regular class
        to_encode = data.__dict__.copy()
    else:
        # This is already a dict or dict-like object
        to_encode = dict(data)
    
    # Convert datetime to timestamp for JWT encoding
    to_encode["exp"] = int(expire.timestamp())
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> TokenClaims:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
