from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .functions import Memory
import os

DATABASE_URL = "jdbc:postgresql://192.168.62.114:5432/postgres"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
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