from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional
from datetime import datetime

class User(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str

    @validator("password")
    def password_requirements(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one number")
        if not any(char.isupper() for char in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char in "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~" for char in v):
            raise ValueError("Password must contain at least one special character")
        return v
    

class Museum(BaseModel):
    name: str
    location: str
    description: Optional[str] = None

class Comment(BaseModel):
    user_id: str
    museum_id: str
    content: str
    timestamp: datetime = datetime.now()

class Rating(BaseModel):
    user_id: str
    museum_id: str
    score: float  # Scale of 1-5

class Ticket(BaseModel):
    user_id: str
    museum_id: str
    purchase_date: datetime = datetime.now()
    visit_date: datetime


