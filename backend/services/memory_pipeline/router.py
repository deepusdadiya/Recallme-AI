from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from alchemist.postgresql.resource import get_db
from .schema import MemoryUploadRequest
from .service import process_memory
from services.auth.dependencies import get_current_user
from alchemist.postgresql.functions import User

router = APIRouter()

@router.post("/upload-memory")
def upload_memory(req: MemoryUploadRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    result = process_memory(db, req.title, req.source_type, req.content, user_id=user.id)
    return {"status": "success", "id": str(result.id)}