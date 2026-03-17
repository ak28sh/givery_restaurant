from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+pymysql://root:password@localhost/restaurant"

try:
    engine = create_engine(DATABASE_URL)
    engine.connect()
    print("Database connection successful")
    SessionLocal = sessionmaker(bind=engine)
except Exception as e:
    print(f"Database connection failed: {e}")

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()