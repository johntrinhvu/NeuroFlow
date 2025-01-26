from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# URL_DATA = 'postgresql://Andrew_login:Cooldue2@localhost:5432/hackathon_db'
URL_DATA = 'postgresql://postgres:476427@localhost:5433/hackathon_db'

engine = create_engine(URL_DATA)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()