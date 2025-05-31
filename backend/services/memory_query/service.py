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

SYSTEM_PROMPT = """
You are Recallme-AI, a concise and intelligent personal memory assistant.

Start by determining the user's intent:

1. **Memory Listing Request**  
   If the query is about listing memories (e.g., “What have I uploaded?”, “Show my memories from today”), return only relevant memory summaries. Format each item as:  
   - title (source_type, summary, created_at: DD Month YYYY)  
   Include `created_at` only if available. Avoid unnecessary details.

2. **Information Search Request**  
   If the query is about retrieving specific information (e.g., “When is my next trip?”, “What did I say about LLM?”), search the memory content and answer directly and precisely. Do not list all matching memories — only respond with the relevant fact or answer derived from context.  
   If a memory contains a `created_at` date and the user asks **"when"**, return an answer like:  
   - “You explored LLM on 29 May 2025.”  
   Keep it short and relevant.

Guidelines:
- Use only contextually relevant memories.
- Do not mention or summarize unrelated entries.
- Never say “based on your memories...” or explain your reasoning.
- If no relevant answer or date is found, respond clearly: “I couldn’t find a memory related to that.”

Your tone should be helpful, clear, and concise.
"""

def list_user_memories(db: Session, user_id: str, filter_by: dict = None):
    query = db.query(Memory).filter(Memory.user_id == user_id)
    if filter_by:
        if "title" in filter_by:
            query = query.filter(Memory.title.ilike(f"%{filter_by['title']}%"))
        if "source_type" in filter_by:
            query = query.filter(Memory.source_type == filter_by["source_type"])

    memories = query.order_by(Memory.created_at.desc()).all()
    if not memories:
        return "No matching memories found."

    memory_lines = [
        f"- {m.title} (source: {m.source_type}, summary: {m.summary or 'No summary'}, created_at: {m.created_at.strftime('%d %B %Y')})"
        for m in memories
    ]
    return "\n".join(memory_lines)


def answer_query(db: Session, query: str, user_id: str, source_type: str = None, title: str = None):
    filters = {"user_id": user_id}
    if source_type:
        filters["source_type"] = source_type
    if title:
        filters["title"] = title

    docs = search_memory_pgvector(db, query, filter_by=filters)

    # Build context from matched docs
    context_blocks = []
    for doc in docs:
        title = doc.metadata.get("title", "Untitled")
        summary = doc.metadata.get("summary", "")
        content = doc.page_content
        context_blocks.append(f"Title: {title}\nSummary: {summary}\nContent: {content}")
    memory_context = "\n\n".join(context_blocks)

    # Get user’s full memory list
    full_memory_list = list_user_memories(db, user_id=user_id, filter_by={"title": "LLM"})

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Here are your relevant memories:\n{full_memory_list}\n\nAnd here is detailed context:\n{memory_context}\n\nQuestion: {query}"}
    ]

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