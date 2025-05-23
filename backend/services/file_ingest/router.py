from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session
from alchemist.postgresql.resource import get_db
from .service import handle_file_upload

router = APIRouter()

@router.post("/upload")
def upload_file(file: UploadFile, db: Session = Depends(get_db)):
    result = handle_file_upload(db, file)
    return {"status": "success", "id": str(result.id)}