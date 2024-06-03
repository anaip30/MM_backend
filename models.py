from pydantic import BaseModel, EmailStr, validator
from typing import  Optional
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



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserInDB(User):
    hashed_password: str


class Rating(BaseModel):
    user_id: str
    museum_id: str = None  
    score: float

    @validator('score')
    def validate_score(cls, value):
        if not 1 <= value <= 5:
            raise ValueError('Rating must be between 1 and 5')
        return value



