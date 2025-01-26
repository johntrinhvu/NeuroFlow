from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, APIRouter
from fastapi.responses import FileResponse
from reportlab.pdfgen import canvas
from models import HRData
import os
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from pydantic import BaseModel
from typing import List
from datetime import datetime
import jwt
import os
import uuid
from models import HRData, User  # Import your HRData model and Base from models
from database import SessionLocal  # Replace with your synchronous session'
from fastapi.security import OAuth2PasswordBearer
from routes.login import active_sessions
import json
import cv2
import numpy as np
from scipy.signal import butter, convolve, find_peaks, filtfilt
from fastapi import FastAPI, Query
import neurokit2 as nk  # Import NeuroKit2 for stress score calculation


from dotenv import load_dotenv
router = APIRouter()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_current_user(db: Session):
    try:
        payload = jwt.decode(active_sessions[0], SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload["user_id"]
        if not user_id:
            raise HTTPException(status_code=401, detail=payload)
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="token")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/hrdata/download")
def download_hr_data(db: Session = Depends(get_db)):
    # Verify the current user
    current_user = get_current_user(db)

    # Query HRData for the current user
    user_hr_data = db.query(HRData).filter(HRData.user_id == current_user.id).all()

    if not user_hr_data:
        raise HTTPException(status_code=404, detail="No HR data found for the user")

    # # Create a temporary PDF file
    # pdf_path = os.path.join(UPLOAD_DIR, f"{current_user.username}_hr_data.pdf")
    # c = canvas.Canvas(pdf_path)

    # # Write HRData to PDF
    # c.setFont("Helvetica", 12)
    # c.drawString(100, 800, f"HR Data for {current_user.username}")
    # y_position = 760

    # for record in user_hr_data:
    #     c.drawString(100, y_position, f"Uploaded At: {record.uploaded_at}")
    #     c.drawString(100, y_position - 20, f"Stress Indicator: {record.stress_indicator}")
    #     c.drawString(100, y_position - 40, f"HR Data: {record.hr_data}")
    #     c.drawString(100, y_position - 60, f"R Avg: {record.r_avg}")
    #     c.line(100, y_position - 80, 500, y_position - 80)
    #     y_position -= 100
    #     if y_position < 100:
    #         c.showPage()  # Add a new page if needed
    #         y_position = 760

    # c.save()

    # Return the PDF as a response
    # return FileResponse(pdf_path, media_type="application/pdf", filename=f"{current_user.username}_hr_data.pdf")
    return user_hr_data