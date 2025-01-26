from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, UploadFile, File, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert
from pydantic import BaseModel
from typing import List, Annotated
from datetime import datetime
import os
import jwt
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, String, Float, JSON, ForeignKey, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from passlib.context import CryptContext
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer


import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")
active_sessions = []


def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})

    print(f"Token payload: {to_encode}")
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# def get_current_user(db: Session):
#     try:
#         payload = jwt.decode(active_sessions[0], SECRET_KEY, algorithms=[ALGORITHM])
#         user_id = payload["user_id"]
#         if not user_id:
#             raise HTTPException(status_code=401, detail=payload)
#         user = db.query(User).filter(User.id == user_id).first()
#         if not user:
#             raise HTTPException(status_code=401, detail="token")
#         return user
#     except jwt.ExpiredSignatureError:
#         raise HTTPException(status_code=401, detail="Token expired")
#     except jwt.PyJWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")
#     except:
#         raise HTTPException(status_code=401, detail="No Login")

# Helper for verifying tokens
def get_current_user(token: str, db: Session):
    try:
        payload = jwt.decode(token, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(model.User).filter(model.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="token")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

app = FastAPI()
router = APIRouter()

# enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class RegisterUser(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginUser(BaseModel):
    email: EmailStr
    password: str

        
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[AsyncSession, Depends(get_db)]

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# @router.options("/users/login")
# def options_login():
#     return {"allow": "POST, OPTIONS"}

@router.post("/users/register")
def register_user(user: RegisterUser, db: db_dependency):
    user_found = db.query(models.User).filter(models.User.username == user.username).first()
    email_found = db.query(models.User).filter(models.User.email == user.email).first()
    if user_found:
        raise HTTPException(status_code=400, detail="Username already exists")
    if email_found:
        raise HTTPException(status_code=400, detail="Email already exists")
    hashed_password = get_password_hash(user.password)
    new_user = models.User(username=user.username, email=user.email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

@router.post("/users/login")
def login_user(user: LoginUser, db: db_dependency):
    db_user = (
        db.query(models.User)
        .filter(models.User.email == user.email)
        .first()
    )
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    print(f"db_user: {db_user}")
    if len(active_sessions) >= 1:  # MODIFY
        raise HTTPException(status_code=403, detail="User already logged in. Please log out first.")
    access_token = create_access_token({"user_id": db_user.id, "name": db_user.username})
    active_sessions.append(access_token)  # MODIFY
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/profile")
def get_profile(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    return {
        "username": current_user.username,
        "email": current_user.email,
        "created_at": current_user.created_at
    }

@router.post("/users/logout")
def logout_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # db_user = get_current_user(token, db)
    # access_token = create_access_token({"user_id": db_user.id, "name": db_user.username})
    global active_sessions

    if len(active_sessions) >= 1:
        active_sessions = []
        return {"message": "Logged out successfully"}
    # if access_token in active_sessions:
    #     del active_sessions[current_user.id]
    else:
        raise HTTPException(status_code=401, detail="No Login")


app.include_router(router, prefix="/users")
