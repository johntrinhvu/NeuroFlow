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

pdfmetrics.registerFont(TTFont('Times-Roman', 'times.ttf'))

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
# Accepts a list of model objects whose attributes can be accessed with "."
# Example percentile data for SDNN, RMSSD, BPM, and Stress Score
percentiles = {
    "SDNN": 70,  # 70th percentile
    "RMSSD": 85,  # 85th percentile
    "pNN50": 50,
    "BPM": 40,    # 40th percentile
    "Stress Score": 30  # 30th percentile
}

test_result = {"sdnn": 50, "rmssd": 51, "pnn50": 100, "bpm": 89, "stress_score": 69}

def generate_stress_report(
    full_name,
    sex,
    test_result, # 
    overall_stress_score,
    clinical_recommendations
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
    
    # Build PDF
    doc.build(content)
    
    # Return PDF as bytes
    return buffer.getvalue()

# Example usage
def example_usage():
    pdf_content = generate_stress_report(
        full_name='Dylan Tran',
        sex="male",
        test_result=test_result,
        overall_stress_score=65,
        clinical_recommendations="Recommend stress management techniques and follow-up consultation."
    )
    
    # Write to file for demonstration
    with open('stress_report.pdf', 'wb') as f:
        f.write(pdf_content)

# Uncomment to test
example_usage()