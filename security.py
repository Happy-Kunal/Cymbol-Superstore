from datetime import datetime, timedelta
import os

from dotenv import load_dotenv, find_dotenv
from pydantic import BaseModel
from fastapi import APIRouter, Query
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database import get_db
import models, schemas


# loading environment variables from .env file
load_dotenv(find_dotenv())

# environment variables
SECRET_KEY = os.environ.get("SECRET_KEY", "FAKE_SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM", "MD5")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


class Token(BaseModel):
    access_token: str
    token_type: str


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



credentials_exception = HTTPException(
    status.HTTP_404_NOT_FOUND,
    detail="username or password is incorrect"
)



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None, seller: bool = False):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire, "seller": seller})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def authenticate_user(username: str, password: str, db: Session = Depends(get_db), seller: bool = False):
    if (seller):
        user = db.query(models.Seller).filter(models.Seller.email == username).first()
    else:
        user = db.query(models.Customer).filter(models.Customer.email == username).first()
    
    if user and verify_password(password, user.hashed_password):
        return user
    else:
        raise credentials_exception
    
    


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), seller: bool = Query(default=False)):
    user = authenticate_user(form_data.username, form_data.password, seller=seller)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires, seller=seller
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/test")
async def test_security():
    return {"ok": True}

