from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv
import os
from models import Item  # Import models here

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Create the engine
engine = create_engine(DATABASE_URL)

# Function to initialize the database
def init_db():
    SQLModel.metadata.create_all(engine)  # Creates tables based on imported models
    print("Database and tables created!")
