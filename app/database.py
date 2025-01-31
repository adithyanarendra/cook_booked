from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database URL from .env file
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the engine using pg8000 for PostgreSQL
engine = create_engine(DATABASE_URL, connect_args={})

# Set up the session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()
