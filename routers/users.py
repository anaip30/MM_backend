from fastapi import APIRouter, HTTPException, status
from models import User
from database import user_collection
from security import get_password_hash

router = APIRouter()

@router.post("/register", response_model=User, response_description="Register a new user")
async def register_user(user: User):
    user_in_db = user_collection.find_one({"username": user.username})
    if user_in_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    user.password = get_password_hash(user.password)  
    user_collection.insert_one(user.dict())
    user.password = "****"  
    return user

@router.get("/users/", response_model=list[User])
async def read_users():
    users = list(user_collection.find({}, {"_password": 0}))  
    return users
