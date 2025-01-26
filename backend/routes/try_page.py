from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, APIRouter
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
from openai import OpenAI

from dotenv import load_dotenv
router = APIRouter()
app = FastAPI()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

# Replace with your OpenAI API key
OPENAI_KEY = os.getenv("OPENAI_KEY")
def generate_chatgpt_response(prompt, max_tokens=100, temperature=0.7):
    """
    Generates a response from ChatGPT based on the given prompt.
    
    Args:
        prompt (str): The input prompt for ChatGPT.
        max_tokens (int): Maximum number of tokens in the response. Default is 100.
        temperature (float): Sampling temperature for response creativity. Default is 0.7.
        
    Returns:
        str: The generated response text.
    """
    try:
        # Call the OpenAI API
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use a valid model name
            messages=[
                {"role": "system", "content": "You are a medical professional and will read Heart rate variability data that correlates with stress."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        # Extract and return the response
        return completion.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"


def create_prompt(bpm, sdnn, rmssd, pnn50, stress_score):
    """
    Creates a prompt for GPT to evaluate biometric characteristics and provide recommendations.
    
    Args:
        bpm (float): Beats Per Minute (BPM)
        sdnn (float): Standard deviation of NN intervals
        rmssd (float): Root mean square of successive differences
        pnn50 (float): Percentage of NN50 intervals
        stress_score (float): Stress score
    
    Returns:
        str: Formatted prompt string
    """
    return f"""
Evaluate the following biometric characteristics:
- BPM: {bpm}
- SDNN: {sdnn}
- RMSSD: {rmssd}
- pNN50: {pnn50}
- Stress Score: {stress_score}

Provide a brief interpretation of these values and give 1–2 actionable recommendations to improve overall well-being. Keep the response short and in a bulleted format.
"""

class NumpyEncoder(json.JSONEncoder):
    """Special JSON encoder for numpy types."""

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype="high", analog=False)
    return b, a


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype="low", analog=False)
    return b, a


def filter_all(data, fs, order=5, cutoff_high=8, cutoff_low=25):
    b, a = butter_highpass(cutoff_high, fs, order=order)
    highpassed_signal = filtfilt(b, a, data)
    d, c = butter_lowpass(cutoff_low, fs, order=order)
    bandpassed_signal = filtfilt(d, c, highpassed_signal)
    return bandpassed_signal


def process_signal(y, order_of_bandpass, high, low, sampling_rate, average_filter_sample_length):
    filtered_signal = filter_all(y, sampling_rate, order_of_bandpass, high, low)
    squared_signal = filtered_signal ** 2
    b = (np.ones(average_filter_sample_length)) / average_filter_sample_length
    a = np.ones(1)
    averaged_signal = convolve(squared_signal, b)
    averaged_signal = filtfilt(b, a, squared_signal)
    return averaged_signal


def calculate_hrv(rr_intervals):
    """Calculate HRV metrics: SDNN, RMSSD, and pNN50."""
    rr_intervals_ms = np.array(rr_intervals) * 1000  # Convert to milliseconds
    sdnn = np.std(rr_intervals_ms)  # Standard deviation of RR intervals
    rmssd = np.sqrt(np.mean(np.diff(rr_intervals_ms) ** 2))  # Root mean square of successive differences
    nn50 = sum(np.abs(np.diff(rr_intervals_ms)) > 50)  # Count of differences > 50ms
    pnn50 = (nn50 / len(rr_intervals_ms)) * 100  # Percentage of NN50 intervals
    return {"SDNN": sdnn, "RMSSD": rmssd, "pNN50": pnn50}


def calculate_stress_score(peak_indices, sampling_rate):
    """Calculate a stress score using NeuroKit2."""
    # Convert peak indices to a binary array (required by NeuroKit2)
    binary_peaks = np.zeros(peak_indices[-1] + 1)  # Create an array the size of the signal
    binary_peaks[peak_indices] = 1  # Set peaks as 1

    # Compute HRV metrics
    hrv_metrics = nk.hrv(binary_peaks, sampling_rate=sampling_rate, show=False)
    stress_index = hrv_metrics.get("HRV_SI", None)  # Stress Index (HRV_SI)
    return stress_index


def give_bpm_and_hrv(averaged, time_bw_fram):
    r_min_peak = min(averaged) + (max(averaged) - min(averaged)) / 16
    r_peaks = find_peaks(averaged, height=r_min_peak)
    total_peaks = len(r_peaks[0])

    if total_peaks <= 1:  # Not enough peaks to calculate BPM
        print("Insufficient peaks detected for BPM and HRV calculation.")
        return {"BPM": 0, "HRV": {"SDNN": 0, "RMSSD": 0, "pNN50": 0}, "Stress_Score": None}

    # Convert peak indices to RR intervals
    rr_intervals = [
        (r_peaks[0][i + 1] - r_peaks[0][i]) * time_bw_fram
        for i in range(total_peaks - 1)
    ]

    avg_time_bw_peaks = np.mean(rr_intervals)
    bpm = float(60.0 / avg_time_bw_peaks)

    # Calculate HRV metrics
    hrv_metrics = calculate_hrv(rr_intervals)

    # Calculate Stress Score using NeuroKit2
    stress_score = calculate_stress_score(r_peaks[0], sampling_rate=int(1 / time_bw_fram))

    return {
        "BPM": bpm,
        "HRV": hrv_metrics,
        "Stress_Score": stress_score
    }

def get_current_user(token: str, db: Session):
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

# Endpoint: Upload video and process HR Data
@router.post("/hrdata/video/upload")
def upload_video(file: UploadFile = File(...), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    current_user = get_current_user(token, db)

    # Save the video to the upload directory
    file_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_{file.filename}")
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    # Validate video file
    if not cv2.VideoCapture(file_path).isOpened():
        raise HTTPException(status_code=400, detail="Video file could not be opened. Please check the format.")

    # Open and process the video file
    video_data = cv2.VideoCapture(file_path)
    fps = video_data.get(cv2.CAP_PROP_FPS)
    frame_count = int(video_data.get(cv2.CAP_PROP_FRAME_COUNT))

    if frame_count == 0:
        raise HTTPException(status_code=400, detail="Video contains no frames.")

    time_bw_frame = 1.0 / fps
    R, G, B = np.array([]), np.array([]), np.array([])

    while True:
        ret, frame = video_data.read()
        if not ret:
            break

        no_of_pixels = 0
        sumr, sumg, sumb = 0.0, 0.0, 0.0  # Initialize as floats

        for i in frame[int((len(frame) - 100) / 2): int((len(frame) + 100) / 2)]:
            for j in i[int((len(frame[0]) - 100) / 2): int((len(frame[0]) + 100) / 2)]:
                sumr += float(j[2])  # Cast to float
                sumg += float(j[1])
                sumb += float(j[0])
                no_of_pixels += 1

        R = np.append(R, sumr / no_of_pixels)
        G = np.append(G, sumg / no_of_pixels)
        B = np.append(B, sumb / no_of_pixels)

    R, G, B = R[100:-100], G[100:-100], B[100:-100]

    r_cutoff_high, r_cutoff_low, r_order_of_bandpass = 10, 100, 5
    r_sampling_rate = 8 * int(fps + 1)
    r_average_filter_sample_length = 7

    r_averaged = process_signal(R, r_order_of_bandpass, r_cutoff_high, r_cutoff_low, r_sampling_rate, r_average_filter_sample_length)

    r_averaged_serializable = r_averaged.tolist()  # Convert to JSON-serializable list
    # Calculate BPM, HRV, and Stress Score
    bpm_and_hrv = give_bpm_and_hrv(r_averaged, time_bw_frame)
    
    new_hr_data = HRData(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        BPM=float(bpm_and_hrv["BPM"]),
        SDNN=float(bpm_and_hrv["HRV"]["SDNN"]), 
        RMSSD=float(bpm_and_hrv["HRV"]["RMSSD"]),
        pNN50=float(bpm_and_hrv["HRV"]["pNN50"]),
        Stress_Score=float(bpm_and_hrv["Stress_Score"][0])
    )
    db.add(new_hr_data)
    db.commit()
    prompt = create_prompt(
        bpm=float(bpm_and_hrv["BPM"]),
        sdnn=float(bpm_and_hrv["HRV"]["SDNN"]),
        rmssd=float(bpm_and_hrv["HRV"]["RMSSD"]),
        pnn50=float(bpm_and_hrv["HRV"]["pNN50"]),
        stress_score=float(bpm_and_hrv["Stress_Score"][0])
    )
    gpt_data = generate_chatgpt_response(prompt)

    return {
        "message": "Video processed successfully",
        "user_id": current_user.id,
        "report_id": new_hr_data.id,
        "BPM" : float(bpm_and_hrv["BPM"]),
        "SDNN": float(bpm_and_hrv["HRV"]["SDNN"]),
        "RMSSD" : float(bpm_and_hrv["HRV"]["RMSSD"]), 
        "pNN50" : float(bpm_and_hrv["HRV"]["pNN50"]),
        "stress_indicator": bpm_and_hrv["Stress_Score"],
        "chatgpt_data" : gpt_data,
    }

# Endpoint: Retrieve HR Data
@router.get("/hrdata/data/{user_id}/{report_id}")
def get_hr_data(user_id: str, report_id: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # validate token
    curr_user = get_current_user(token, db)
    if curr_user.id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized Access")

    # Fetch HR data
    hr_record = db.query(HRData).filter(HRData.user_id == user_id, HRData.id == report_id).first()
    if not hr_record:
        raise HTTPException(status_code=404, detail="Report not found")

    return {
        "BPM": hr_record.BPM,
        "SDNN": hr_record.SDNN,
        "RMSSD": hr_record.RMSSD,
        "pNN50": hr_record.pNN50,
        "stress_indicator": hr_record.Stress_Score,
    }

@router.get("/hrdata/data/{user_id}")
def get_all_hr_data(user_id: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Validate the token and ensure the user matches
    current_user = get_current_user(token, db)
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized access")

    # Fetch all HR data for the user
    hr_records = db.query(HRData).filter(HRData.user_id == user_id).all()
    return {"hr_data": [hr.to_dict() for hr in hr_records]}


app.include_router(router, prefix="/hrdata")