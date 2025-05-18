from pydantic import BaseModel
from enum import Enum

class UploadType(str, Enum):
    text = "text"
    image = "image"
    audio = "audio"
    pdf = "pdf"

class MemoryUploadRequest(BaseModel):
    title: str
    source_type: UploadType
    content: str  # can be base64 or raw text