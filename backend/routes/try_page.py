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
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[AsyncSession, Depends(get_db)]

@router.post("/try")
async def upload_and_process_video(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type not in ["video/mp4", "video/avi", "video/mov"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    processed_data = process_video(file_path)
    
    new_user = User(
        name=processed_data["name"],
        status=processed_data["status"],
        avg_ppg=processed_data["avg_ppg"],
        heart_rate_var=processed_data["heart_rate_var"],
        bpm=processed_data["bpm"]
    )
    db.add(new_user)
    db.commit()
    
    return {"message": "Video uploaded and processed successfully.", "data": processed_data}

def process_video(file_path: str) -> dict:
    # Example simulated results
    return {
        "name": "John Doe",
        "status": "Healthy",
        "avg_ppg": 85.3,
        "heart_rate_var": 0.12,
        "bpm": 72
    }
