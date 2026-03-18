import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables
load_dotenv()

# Get DB URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

print(DATABASE_URL)

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env")

# Create engine
engine = create_engine(DATABASE_URL)

print("Database connection successful")

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def get_db():
    """
    Dependency to get DB session.
    Ensures session is closed after request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()