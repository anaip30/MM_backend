import os
from fastapi import APIRouter, HTTPException, status,  Depends, FastAPI, HTTPException
from models import User
from database import user_collection
from security import get_password_hash, get_current_active_user, create_access_token, authenticate_user
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from models import Token 
from datetime import datetime, timedelta
router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post("/register", response_model=User, response_description="Register a new user")
async def register_user(user: User):
    user_in_db = user_collection.find_one({"username": user.username})
    if user_in_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    user.password = get_password_hash(user.password)  
    user_collection.insert_one(user.dict())
    return user
    

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]