# backend/api/main.py
from fastapi import FastAPI, UploadFile, File
from backend.services.memory_pipeline import process_file
from uuid import uuid4

app = FastAPI()

# Dummy user for local dev
DUMMY_USER_ID = 1

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    memory_id = str(uuid4())
    result = await process_file(file, DUMMY_USER_ID, memory_id)
    return {"status": "success", "memory_id": memory_id, "summary": result}