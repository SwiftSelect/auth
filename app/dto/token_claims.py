from pydantic import BaseModel

class TokenClaims(BaseModel):
    email: str
    role: int
    fullname: str