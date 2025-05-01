from pydantic import BaseModel

class TokenClaims(BaseModel):
    email: str
    role: str
    firstname: str
    lastname: str