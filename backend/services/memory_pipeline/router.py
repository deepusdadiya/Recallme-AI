from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from alchemist.postgresql.resource import get_db
from .schema import MemoryUploadRequest
from .service import process_memory

router = APIRouter()

@router.post("/upload-memory")
def upload_memory(req: MemoryUploadRequest, db: Session = Depends(get_db)):
    result = process_memory(db, req.title, req.source_type, req.content)
    return {"status": "success", "id": str(result.id)}