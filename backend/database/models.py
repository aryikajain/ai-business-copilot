# Data models will be implemented here
from pydantic import BaseModel

class User(BaseModel):
    email: str
    password: str