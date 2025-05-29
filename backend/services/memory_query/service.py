from vectorstore.pgvector_service import search_memory_pgvector
from sqlalchemy.orm import Session
from groq import Groq
import httpx
import os
from uuid import UUID
from alchemist.postgresql.functions import Memory
from dotenv import load_dotenv
load_dotenv()

grok_api_key = os.getenv("GROQ_API_KEY")
insecure_http_client = httpx.Client(verify=False)

client = Groq(
    api_key=grok_api_key,
    http_client=insecure_http_client
)

SYSTEM_PROMPT = """You are Recallme-AI. First determine if the user is asking to list all their memories, or search for content inside them.

If the question is about listing memories (like 'what is my memory from today' or 'show what I've uploaded'), respond with a list of stored memories (titles, source type, summaries).

If the question is asking for information (like 'when is my next trip'), search context and give an answer based on the content of the uploaded memories."""

def list_user_memories(db: Session):
    memories = db.query(Memory).order_by(Memory.created_at.desc()).all()

    if not memories:
        return {
            "answer": "You haven't uploaded any memories yet.",
            "matches": []
        }

    memory_lines = [
        f"- {m.title} (source: {m.source_type}, summary: {m.summary or 'No summary'})"
        for m in memories
    ]

    memory_context = "\n".join(memory_lines)
    return memory_context

def answer_query(db: Session, query: str, source_type: str = None, title: str = None):
    # 1. Vector search results
    filters = {}
    if source_type:
        filters["source_type"] = source_type
    if title:
        filters["title"] = title

    docs = search_memory_pgvector(db, query, filter_by=filters)

    # 2. Prepare memory context for LLM (raw chunks + summaries)
    context_blocks = []
    for doc in docs:
        title = doc.metadata.get("title", "Untitled")
        summary = doc.metadata.get("summary", "")
        content = doc.page_content
        context_blocks.append(f"Title: {title}\nSummary: {summary}\nContent: {content}")
    memory_context = "\n\n".join(context_blocks)

    # 3. Include full memory list as background context
    full_memory_list = list_user_memories(db)

    # 4. Construct prompt
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": f"Here is the list of your stored memories:\n{full_memory_list}\n\nNow, based on this context:\n{memory_context}\n\nQuestion:\n{query}"
        }
    ]

    # 5. Call Groq LLM
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=messages,
        temperature=0,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )

    answer = completion.choices[0].message.content

    def convert_metadata(metadata: dict):
        return {
            k: str(v) if isinstance(v, UUID) else v
            for k, v in metadata.items()
        }

    return {
        "answer": answer,
        "matches": [
            {
                "content": doc.page_content,
                "metadata": convert_metadata(doc.metadata)
            }
            for doc in docs
        ]
    }