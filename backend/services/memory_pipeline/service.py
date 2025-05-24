from config.config import DUMMY_USER_ID
from vectorstore.faiss_service import store_text
from alchemist.postgresql.initializer import SourceType
from alchemist.postgresql.resource import save_memory
from services.memory_pipeline.summarizer import summarize_text

def process_memory(db, title: str, source_type: str, raw_text: str):
    summary = summarize_text(raw_text)
    memory_data = {
        "user_id": DUMMY_USER_ID,
        "title": title,
        "source_type": SourceType(source_type),
        "raw_text": raw_text,
        "summary": summary
    }
    memory = save_memory(db, memory_data)
    store_text(text=raw_text, metadata={"memory_id": str(memory.id), "title": title})
    return memory