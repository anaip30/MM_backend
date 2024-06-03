from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel
from models import User, TokenData, UserInDB
from database import user_collection

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") 

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user( username: str):
    user = user_collection.find_one({
    "username":username,})
    if user:
        user["hashed_password"]=user["password"]
        return UserInDB(**user)
        

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
    user = get_user(username=token_data.username)
    if user is None:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
     return current_user

def authenticate_user(username: str, password: str):
    user = get_user(username)
    hashed_password = user.password
    if not user or not verify_password(password, hashed_password):
        return False
    return user