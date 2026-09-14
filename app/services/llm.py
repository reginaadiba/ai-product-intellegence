import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not configured")

client = genai.Client(
    api_key=GEMINI_API_KEY
)


def generate_answer(prompt: str) -> str:
    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt,
    )

    return interaction.output_text