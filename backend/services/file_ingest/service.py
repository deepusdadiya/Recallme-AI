import os
import tempfile
import subprocess
from fastapi import UploadFile
from services.memory_pipeline.service import process_memory
from alchemist.postgresql.initializer import SourceType
from PIL import Image
import pytesseract
import fitz

def get_file_extension(filename: str) -> str:
    return filename.rsplit(".", 1)[-1].lower()

def detect_file_type(extension: str):
    ext = extension.lower()
    if ext in ["png", "jpg", "jpeg", "bmp", "tiff"]:
        return "image"
    if ext in ["mp3", "wav", "m4a"]:
        return "audio"
    if ext in ["mp4", "mov", "avi", "mkv"]:
        return "video"
    if ext == "pdf":
        return "pdf"
    if ext == "txt":
        return "text"
    return "unknown"

def extract_text_from_image(file_path: str) -> str:
    image = Image.open(file_path)
    return pytesseract.image_to_string(image)

def extract_text_from_audio(file_path: str) -> str:
    import whisper
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    return result["text"]

def extract_audio_from_video(video_path: str, output_audio_path: str):
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-q:a", "0",
        "-map", "a",
        "-y",
        output_audio_path
    ]
    subprocess.run(cmd, check=True)

def extract_text_from_video(file_path: str) -> str:
    audio_path = file_path + ".wav"
    extract_audio_from_video(file_path, audio_path)
    text = extract_text_from_audio(audio_path)
    os.remove(audio_path)
    return text

def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def handle_file_upload(db, file: UploadFile):
    suffix = os.path.splitext(file.filename)[1]
    extension = suffix.lstrip('.')
    file_type = detect_file_type(extension)
    print("Detected file type:", file_type)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(file.file.read())
        temp_file_path = temp_file.name

    try:
        if file_type == "image":
            text = extract_text_from_image(temp_file_path)
        elif file_type == "audio":
            text = extract_text_from_audio(temp_file_path)
        elif file_type == "video":
            text = extract_text_from_video(temp_file_path)
        elif file_type == "pdf":
            text = extract_text_from_pdf(temp_file_path)
        elif file_type == "text":
            text = extract_text_from_txt(temp_file_path)
        else:
            raise ValueError("Unsupported file type.")

        memory = process_memory(
            db,
            title=file.filename,
            source_type=file_type,
            raw_text=text
        )
        return memory

    finally:
        os.remove(temp_file_path)