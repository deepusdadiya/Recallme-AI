import os
import httpx
from dotenv import load_dotenv
from groq import Groq
import re

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

client = Groq(
    api_key=api_key,
    http_client=httpx.Client(verify=False)
)

def clean_extracted_text(text: str) -> str:
    text = re.sub(r'\n{2,}', '\n', text)
    text = re.sub(r'\s{2,}', ' ', text)
    text = text.replace('|', '-')
    return text.strip()

def summarize_text(text: str) -> str:
    system_prompt = f"""
    You are a memory summarizer for a digital vault. Return the summary of the input.

    Summarize the following text concisely. Your summary should include:
    - Type of document (e.g., Uber receipt, bank statement)
    - Key details (date, time, location, names, amounts, etc.)
    - Mention monetary values, IDs, or plate numbers if present

    Avoid vague phrases. Be specific but brief.

    Do not prefix with anything like 'Here is a summary' or 'Let me give you the summary'.
    Return only the result as plain text. Nothing else.

    For Example, if the input is:
    'We discussed the timeline for feature rollout and agreed on pushing the release to Q3. The UI team will submit designs by end of this week.'

    Then return:
    'Feature rollout timeline discussion, Agreed on pushing to Q3, UI team will submit designs by end of this week'
    
    Text:
    \"\"\"
    {text[:3000]}
    \"\"\"
    """

    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{"role": "system", "content": system_prompt}],
            temperature=0.3,
            max_completion_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("Summarization failed:", e)
        return None