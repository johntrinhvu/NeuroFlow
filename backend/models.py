from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, JSON
from datetime import datetime
from database import Base
import uuid

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class HRData(Base):
    __tablename__ = "hr_data"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    BPM = Column(Float, nullable=False)
    SDNN = Column(Float, nullable=False)
    RMSSD = Column(Float, nullable=False)
    pNN50 = Column(Float, nullable=False)
    Stress_Score = Column(Float, nullable=False)
