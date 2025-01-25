from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, APIRouter
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from pydantic import BaseModel
from typing import List
from datetime import datetime
import os
import uuid
from models import HRData, Base  # Import your HRData model and Base from models
from database import SessionLocal  # Replace with your synchronous session

router = APIRouter()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Helper function to process the video
def process_video_for_hr(video_file):
    # Replace with actual video processing logic
    mock_hr_data = {
        "average_rr": 0.75,
        "sdnn": 45.6,
        "rmssd": 32.1
    }
    stress_indicator = "Low" if mock_hr_data["sdnn"] > 40 else "High"
    return mock_hr_data, stress_indicator

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint: Upload video and process HR Data
@router.post("/hrdata/video/upload")
def upload_video(file: UploadFile = File(...), user_id: str = Depends(get_db), db: Session = Depends(get_db)):
    if not user_id:
        raise HTTPException(status_code=401, detail="User not logged in")

    # Save the video to the upload directory
    file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_{file.filename}")
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    # Process video for HR data
    hr_data, stress_indicator = process_video_for_hr(file_path)

    # Store HR data in database
    new_hr_data = HRData(
        id=str(uuid.uuid4()),
        user_id=user_id,
        uploaded_at=datetime.utcnow(),
        hr_data=hr_data,
        stress_indicator=stress_indicator
    )
    db.add(new_hr_data)
    db.commit()

    return {
        "message": "Video processed successfully",
        "stress_indicator": stress_indicator
    }

# Endpoint: Retrieve HR Data
@router.get("/hrdata/data")
def get_hr_data(user_id: str = Depends(get_db), db: Session = Depends(get_db)):
    result = db.execute(select(HRData).filter(HRData.user_id == user_id))
    hr_records = result.scalars().all()
    return {"hr_data": hr_records}
