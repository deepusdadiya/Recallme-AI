from fastapi import APIRouter, UploadFile, Depends, Security
from sqlalchemy.orm import Session
from alchemist.postgresql.resource import get_db
from .service import handle_file_upload
from services.auth.dependencies import get_current_user
from alchemist.postgresql.functions import User
from fastapi.responses import FileResponse
from uuid import UUID
import os
from fastapi import HTTPException

router = APIRouter()

@router.post("/upload")
def upload_file(file: UploadFile, db: Session = Depends(get_db), current_user: User = Security(get_current_user)):
    result = handle_file_upload(db, file, user_id=current_user.id)
    return {"status": "success", "id": str(result.id)}


@router.get("/files/{filename}")
def serve_file(filename: str):
    file_path = os.path.join("uploaded_files", filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=file_path, filename=filename)


@router.post("/extract-text")
def extract_text_preview(file: UploadFile):
    from .service import extract_text_from_image, detect_file_type
    import tempfile, os

    ext = os.path.splitext(file.filename)[1]
    print("File extension:", ext)
    suffix = os.path.splitext(file.filename)[1]
    ext = suffix.lstrip('.')
    file_type = detect_file_type(ext)
    print("Detected file type:", file_type)

    if file_type != "image":
        return {"error": "Only image files are supported in this endpoint."}

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp:
        temp.write(file.file.read())
        temp_path = temp.name

    text = extract_text_from_image(temp_path)
    os.remove(temp_path)

    return {"extracted_text": text}