from pydantic import BaseModel

class UserSignup(BaseModel):
    email: str
    firstName: str
    lastName: str
    password: str
    role: int