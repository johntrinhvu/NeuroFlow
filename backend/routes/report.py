from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, APIRouter
from fastapi.responses import FileResponse
from reportlab.lib.utils import ImageReader
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
import matplotlib
matplotlib.use('Agg')

from hrv_data import hrv_data
from scipy.stats import norm
import matplotlib.pyplot as plt
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import math
from reportlab.platypus import Image
from openai import OpenAI

import matplotlib.pyplot as plt



# pdfmetrics.registerFont(TTFont('Times-Roman', 'times.ttf'))


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
def format_data_for_prompt(data):
    formatted_data = "You are a medical professional and will read Heart rate variability data that correlates with stress. Here are the patient's HRV metrics:\n\n"
    formatted_data += f"{data[0][0]:<10} | {data[0][1]:<10} | {data[0][2]:<10} | {data[0][3]:<10}\n"
    formatted_data += "-" * 50 + "\n"
    for row in data[1:]:
        formatted_data += f"{row[0]:<10} | {row[1]:<10} | {row[2]:<10} | {row[3]:<10}\n"
    return formatted_data

def generate_chatgpt_recommendation(data):
    client = OpenAI(
        api_key=OPENAI_KEY,  # This is the default and can be omitted
    )
    formatted_data = format_data_for_prompt(data)
    prompt = (
        f"{formatted_data}\n\n"
        "Based on these results, provide a brief interpretation of the metrics and recommend 1–2 actionable steps the patient should take to improve their overall well-being. Do it in a simple text format so no formating with headers or subheaders or anything like that, just plain text."
    )
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4o",
    )
    return chat_completion.choices[0].message.content

def create_stress_score_plot(date_to_stress_score):
    """
    Generate a line plot for stress scores over time.
    Args:
        date_to_stress_score (dict): Dictionary of date-time to stress score.

    Returns:
        bytes: The graph as an image in bytes.
    """
    # Extract dates and stress scores
    dates = list(date_to_stress_score.keys())
    scores = list(date_to_stress_score.values())
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(dates, scores, marker="o", linestyle="-")
    plt.title("Stress Score Over Time")
    plt.xlabel("Date")
    plt.ylabel("Stress Score")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    
    # Save the plot to a BytesIO buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    plt.close()
    buffer.seek(0)
    return buffer


def calculate_percentile(sex, measurement_type, measurement):
    # sex = "male" or "female"
    # Measurement type = "SDNN", "RMSSD", "pNN50", "BPM"
    percentile = 0
    pop_mean = 0
    std_dev = 0
    
    pop_mean = hrv_data[measurement_type][sex]["value"]
    std_dev = hrv_data[measurement_type][sex]["std_dev"]

    z_score = (measurement - pop_mean) / std_dev
    percentile = norm.cdf(z_score) * 100
    print(percentile)
    return round(percentile, 2)

def generate_stress_report(
    full_name,
    sex,
    test_result, # 
    overall_stress_score,
    clinical_recommendations,
    stress_score_plot
):
    """
    Generate a stress report PDF document
    
    Args:
        Various parameters for stress test metrics and explanations
    
    Returns:
        bytes: PDF document content
    """

    percentiles = {
        "SDNN": calculate_percentile(sex, "SDNN", test_result["sdnn"]),  # 70th percentile
        "RMSSD": calculate_percentile(sex, "RMSSD", test_result["rmssd"]),  # 85th percentile
        "pNN50": calculate_percentile(sex, "PNN50", test_result["pnn50"]),
        "BPM": calculate_percentile(sex, "BPM", test_result["bpm"]),    # 40th percentile
        "Stress Score": test_result["stress_score"]  # 30th percentile
    }

    intervals = {
        "SDNN": str(hrv_data["SDNN"][sex]["value"]) + " ±" + str(hrv_data["SDNN"][sex]["std_dev"]),
        "RMSSD": str(hrv_data["RMSSD"][sex]["value"]) + " ±" + str(hrv_data["RMSSD"][sex]["std_dev"]),
        "pNN50": str(hrv_data["PNN50"][sex]["value"]) + " ±" + str(hrv_data["PNN50"][sex]["std_dev"]),
        "BPM": str(hrv_data["BPM"][sex]["value"]) + " ±" + str(hrv_data["BPM"][sex]["std_dev"]),
        "Stress Score": "50 ± 10"
    }
    # Create a buffer to store PDF
    buffer = io.BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle', 
        parent=styles['Title'], 
        fontName='Times-Roman', 
        fontSize=16
    )
    heading_style = ParagraphStyle(
        'HeadingStyle', 
        parent=styles['Heading2'], 
        fontName='Times-Bold', 
        fontSize=12
    )
    centered_heading_style = ParagraphStyle(
        'HeadingStyle', 
        parent=styles['Heading2'], 
        fontName='Times-Roman', 
        fontSize=12,
        alignment=1
    )
    normal_style = ParagraphStyle(
        'NormalStyle', 
        parent=styles['Normal'], 
        fontName='Times-Roman', 
        fontSize=10
    )
    normal_style_bold = ParagraphStyle( 
        'NormalStyle', 
        parent=styles['Normal'], 
        fontName='Times-Bold',  # Make the font bold
        fontSize=10
    )

    
    # Prepare content
    content = []
    
    # Title
    content.append(Paragraph("Neuroflow Stress Test Report", title_style))
    
    # Metadata

    current_time = datetime.now().strftime("%m/%d/%Y %H:%M")

    content.append(Paragraph("Patient Name: " + full_name, heading_style))
    content.append(Paragraph("Report Date: " + current_time, heading_style))

    # Metrics Table
    data = [
        ['Metric', 'Result', 'Interval', 'Percentile'],
        ['SDNN', test_result["sdnn"], intervals["SDNN"], percentiles["SDNN"]],
        ['RMSSD', test_result["rmssd"], intervals["RMSSD"], percentiles["RMSSD"]],
        ['pNN50', test_result["pnn50"], intervals["pNN50"], percentiles["pNN50"],],
        ['BPM', test_result["bpm"], intervals["BPM"], percentiles["BPM"]]
    ]
    
    # Create table with styling
    table = Table(data, colWidths=[100, 100, 100, 200])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    
    content.append(table)
    
    # Overall Stress Score
    content.append(Paragraph(f"Overall Stress Score: {overall_stress_score}/100", centered_heading_style))
    
    # Interpretation
    content.append(Paragraph("Interpretation", heading_style))
    content.append(Paragraph("SDNN", heading_style))
    content.append(Paragraph("This number shows whether or not your variability is within the standard overall range. Higher numbers usually indicate that your body is coping better with stress.\n", normal_style))
    content.append(Paragraph("RMSSD", heading_style))
    content.append(Paragraph("This reflects parasympathetic activity. Higher numbers indicate restfulness.\n", normal_style))
    content.append(Paragraph("pNN50", heading_style))
    content.append(Paragraph("This reflects how active the parasympathetic system is relative to the sympathetic nervous system. The higher the value, the more relaxed the body is. Low pNN50 values indicate tiredness or high-stress.\n", normal_style))
    content.append(Paragraph("BPM", heading_style))
    content.append(Paragraph("This reflects the number of heartbeats per minute. BPMs fluctuate with physical activity, but lower numbers indicate higher fitness levels.\n", normal_style))

    # Clinical Recommendations
    content.append(Paragraph("Clinical Recommendations:", heading_style))
    content.append(Paragraph(clinical_recommendations, normal_style))
    
    recommendation = generate_chatgpt_recommendation(data)
    # Add ChatGPT Recommendations
    content.append(Paragraph("Additional AI-Based Recommendations:", heading_style))
    content.append(Paragraph(recommendation, normal_style))
 
    # Add Graph
    if stress_score_plot:
        image = Image(stress_score_plot, width=400, height=300)  # Adjust width and height as needed
        content.append(image)
    
    # Build PDF
    doc.build(content)
    
    # Return PDF as bytes
    return buffer.getvalue()

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

    # Prepare data for the graph
    date_to_stress_score = {}
    for hdr in user_hr_data:
        timestamp = hdr.uploaded_at
        formatted_datetime = str(timestamp.strftime("%Y-%m-%d %H:%M"))
        date_to_stress_score[formatted_datetime] = hdr.Stress_Score

    # Generate the graph
    stress_score_plot = create_stress_score_plot(date_to_stress_score)

    # Prepare the most recent test result
    most_recent_hdr = user_hr_data[-1]
    test_result = {
        "sdnn": most_recent_hdr.SDNN,
        "rmssd": most_recent_hdr.RMSSD,
        "pnn50": most_recent_hdr.pNN50,
        "bpm": most_recent_hdr.BPM,
        "stress_score": most_recent_hdr.Stress_Score,
    }

    # Generate the PDF
    pdf_content = generate_stress_report(
        full_name="Dylan Tran",
        sex="male",
        test_result=test_result,
        overall_stress_score=65,
        clinical_recommendations="Recommend stress management techniques and follow-up consultation.",
        stress_score_plot=stress_score_plot,
    )

    # Write the PDF file
    file_path = "stress_report.pdf"
    with open(file_path, "wb") as f:
        f.write(pdf_content)

    # Return the file as a response
    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename="stress_report.pdf"
    )

    
app.include_router(router, prefix="/hrdata")