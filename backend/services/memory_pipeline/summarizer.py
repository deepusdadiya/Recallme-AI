import os
import httpx
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

client = Groq(
    api_key=api_key,
    http_client=httpx.Client(verify=False)
)

def summarize_text(text: str) -> str:
    if len(text.split()) > 10:
        text = " ".join(text.split()[:10])

    system_prompt = (
    "You are a summarization engine. Return only the core summary of the input." \
    "Do not prefix with anything like 'Here is a summary' or 'Let me give you the summary'." \
    "Return only the result as plain text. Nothing else." \
    "For Example, if the input is 'We discussed the timeline for feature rollout and agreed on pushing the release to Q3." \
    "The UI team will submit designs by end of this week.', then return only 'Agreed on feature rollout timeline.' " \
    "Not like 'Here is a summary: Agreed on feature rollout timeline.' "
)
    user_prompt = f"{text}"

    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_completion_tokens=512
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("Summarization failed:", e)
        return None