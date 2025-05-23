from pydantic import BaseModel
from enum import Enum

class FileType(str, Enum):
    image = "image"
    audio = "audio"
    video = "video"
    pdf = "pdf"
    text = "text"
    unknown = "unknown"