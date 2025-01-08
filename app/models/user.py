# models/user.py
from typing import Optional

from pydantic import BaseModel, EmailStr

class User(BaseModel):
    first_name: str
    last_name: str
    city: str
    username: str
    email: EmailStr
    password: str
    role : str = "user" # default user is set to the user role
    is_active : bool = False

    class Config:
        orm_mode = True


