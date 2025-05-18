from sqlalchemy.orm import Session
from .functions import Memory

def save_memory(db: Session, memory_data: dict):
    db_memory = Memory(**memory_data)
    db.add(db_memory)
    db.commit()
    db.refresh(db_memory)
    return db_memory