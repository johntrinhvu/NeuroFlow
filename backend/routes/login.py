from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, UploadFile, File, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert
from pydantic import BaseModel
from typing import List, Annotated
from datetime import datetime
import os
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, String, Float, JSON, ForeignKey, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from passlib.context import CryptContext
from typing import Annotated

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class RegisterUser(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginUser(BaseModel):
    username: str
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

# --- User Routes ---
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
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "user_id": db_user.id}

@router.get("/users/profile")
def get_profile(user_id: str, db:db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at
    }