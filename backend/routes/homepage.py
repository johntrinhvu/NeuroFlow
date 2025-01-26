from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, UploadFile, File, APIRouter
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

router = APIRouter()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[AsyncSession, Depends(get_db)]

@router.get("/")
def homepage(db: Session = Depends(get_db)):
    return {
        "message": "Welcome to the HR Data Analysis App!",
        "total_videos_processed": total_videos,
        "average_tiredness_score": average_tiredness,
    }
