from pydantic import BaseModel

class UserSignup(BaseModel):
    email: str
    firstname: str
    lastname: str
    password: str
    role: int