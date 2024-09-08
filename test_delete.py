import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, DashboardData, CompanyData, TransportData
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Set up SQLite database connection
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

session = SessionLocal()

session.query(DashboardData).delete()
session.query(CompanyData).delete()
session.query(TransportData).delete()
session.commit()  # Commit the changes to the database

