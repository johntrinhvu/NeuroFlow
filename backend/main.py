from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, UploadFile, File
from routes import homepage_router, try_page_router, login_router, report_router
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert
from pydantic import BaseModel
from typing import List, Annotated
from datetime import datetime
import os
import uuid
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

# class UserBase(BaseModel):
#     name: str
#     status: str
#     avg_ppg: float
#     heart_rate_var: float
#     bpm: int


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[AsyncSession, Depends(get_db)]

# @app.get("/users/{user_id}")
# async def create_user(user_id: int, db:db_dependency):
#     result = db.query(models.User).filter(models.User.id == question_id).first()
#     if not results:
#         raise HTTPException(status_code=404, detail='user not found')
#     return result

# @app.post("/users/")
# async def create_user(user: UserBase, db:db_dependency):
#     db_user = models.User(name=user.name, status=user.status, avg_ppg=user.avg_ppg, heart_rate_var=user.heart_rate_var, bpm=user.bpm)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)

app.include_router(homepage_router)
app.include_router(try_page_router)
app.include_router(login_router)
app.include_router(report_router)