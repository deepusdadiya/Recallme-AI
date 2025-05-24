from vectorstore.faiss_service import search_memory
from groq import Groq
import httpx
import os
from dotenv import load_dotenv
load_dotenv()

grok_api_key = os.getenv("GROQ_API_KEY")

insecure_http_client = httpx.Client(verify=False)

client = Groq(
    api_key=grok_api_key,
    http_client=insecure_http_client
)

def answer_query(query: str):
    # 1. Search similar memory chunks
    docs = search_memory(query)
    context = "\n\n".join([doc.page_content for doc in docs])

    # 2. Prepare chat prompt
    messages = [
        {
            "role": "system",
            "content": "You are Recallme-AI, a personal memory assistant that uses past uploaded notes to answer user questions clearly and concisely."
        },
        {
            "role": "user",
            "content": f"Based on the following context, answer this question.\n\nCONTEXT:\n{context}\n\nQUESTION:\n{query}"
        }
    ]

    # 3. Call Groq LLM
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=messages,
        temperature=0,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )

    # 4. Extract answer
    answer = completion.choices[0].message.content

    return {
        "answer": answer,
        "matches": [
            {"content": doc.page_content, "metadata": doc.metadata}
            for doc in docs
        ]
    }