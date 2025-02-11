from pydantic import BaseModel

class ValidateUser(BaseModel):
    token: str
    action: str
