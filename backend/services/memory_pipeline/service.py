from config.config import DUMMY_USER_ID
from vectorstore.pgvector_service import store_text_pgvector
from alchemist.postgresql.initializer import SourceType
from alchemist.postgresql.resource import save_memory
from services.memory_pipeline.summarizer import summarize_text
from textwrap import wrap

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
    # Split text into chunks (e.g., ~500 tokens or 2000 characters)
    chunks = wrap(raw_text, 2000)

    for i, chunk in enumerate(chunks):
        store_text_pgvector(
            db,
            text=chunk,
            metadata={
                "memory_id": str(memory.id),
                "title": title,
                "summary": summary,
                "chunk_index": i
            }
        )
    return memory