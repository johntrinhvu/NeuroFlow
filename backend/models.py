from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    status = Column(String, index=True)
    avg_ppg = Column(Float, index=True)
    heart_rate_var = Column(Float, index=True)
    bpm = Column(Integer, index=True)

