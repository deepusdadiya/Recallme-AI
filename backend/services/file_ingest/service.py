import os
import tempfile
import subprocess
from fastapi import UploadFile
from services.memory_pipeline.service import process_memory
from alchemist.postgresql.initializer import SourceType
from PIL import Image
import pytesseract
import fitz
import uuid
import io
from PIL import Image, ImageFilter
import pytesseract
import cv2


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
    # Load image using OpenCV
    image = cv2.imread(file_path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding (better than fixed threshold)
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 31, 10
    )

    # Optional: Remove noise and smooth the image
    denoised = cv2.medianBlur(thresh, 3)

    # Save preprocessed image temporarily for OCR
    is_success, im_buf_arr = cv2.imencode(".png", denoised)
    img_bytes = im_buf_arr.tobytes()
    image_for_ocr = Image.open(io.BytesIO(img_bytes))
    image_for_ocr = image_for_ocr.filter(ImageFilter.SHARPEN)


    # Run OCR
    custom_config = r'--oem 3 --psm 6'  # LSTM engine, assume block of text
    text = pytesseract.image_to_string(image_for_ocr, config=custom_config, lang='eng+hin')

    return text.strip()


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
    extracted_text = ""

    with fitz.open(file_path) as doc:
        for page_number in range(len(doc)):
            page = doc[page_number]
            text = page.get_text().strip()

            # If no text found, fallback to OCR
            if not text:
                print(f"Page {page_number + 1} had no text. Using OCR.")
                pix = page.get_pixmap(dpi=300)
                img_data = pix.tobytes("png")

                # Convert to PIL image and run Tesseract
                image = Image.open(io.BytesIO(img_data))
                ocr_text = pytesseract.image_to_string(image, lang="eng")
                extracted_text += ocr_text + "\n"
                print("extracted text from pdf", extracted_text)
            else:
                extracted_text += text + "\n"
                print("extracted text from pdf", extracted_text)
    print("Total characters extracted from PDF:", len(extracted_text))
    return extracted_text.strip()


def extract_text_from_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def handle_file_upload(db, file: UploadFile, user_id: int):
    suffix = os.path.splitext(file.filename)[1]
    extension = suffix.lstrip('.')
    file_type = detect_file_type(extension)
    print("Detected file type:", file_type)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(file.file.read())
        temp_file_path = temp_file.name

    UPLOAD_DIR = "uploaded_files"
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    filename = f"{uuid.uuid4()}{suffix}"
    saved_path = os.path.join(UPLOAD_DIR, filename)

    with open(saved_path, "wb") as out_file:
        out_file.write(file.file.read())

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
            raw_text=text,
            user_id=user_id
        )
        return memory
    finally:
        os.remove(temp_file_path)