from pydantic import BaseModel, Field
from typing import Optional

class Org(BaseModel):
    id: int
    name: str
    domain: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserLoginResponse(BaseModel):
    access_token: str
    refresh_token: str

class UserResponse(BaseModel):
    id: int
    email: str
    firstname: str
    lastname: str
    role_id: int
    org: Optional[Org]
    class Config:
        orm_mode = True