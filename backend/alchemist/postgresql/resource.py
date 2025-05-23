from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .functions import Memory
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
load_dotenv()

# Load environment variables
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_memory(db: Session, memory_data: dict):
    db_memory = Memory(**memory_data)
    db.add(db_memory)
    db.commit()
    db.refresh(db_memory)
    return db_memory