from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# DATABASE_URL = "mysql+pymysql://root:password@localhost/restaurant"
# engine = create_engine(DATABASE_URL)

# DATABASE_URL = "sqlite:///./restaurant.db"
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

DATABASE_URL = "mysql+pymysql://root:BBKUArAGwCWGgoASdzLQZfHxPxsCUyWx@caboose.proxy.rlwy.net:24476/railway"
engine = create_engine(DATABASE_URL)


print("Database connection successful")
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()