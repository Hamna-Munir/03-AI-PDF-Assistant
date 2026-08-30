"""
assistant.py
Core logic: sends a prompt (with document context) to Groq and returns
the text response. Same pattern used in Week 2.
"""

from openai import OpenAI
from src.config import GROQ_API_KEY, GROQ_BASE_URL, GROQ_MODEL
from src.prompts import GROUNDED_SYSTEM_PROMPT

client = OpenAI(api_key=GROQ_API_KEY, base_url=GROQ_BASE_URL)


def get_answer(prompt: str, temperature: float = 0.2, max_tokens: int = 500) -> str:
    """
    Sends a grounded Q&A prompt to Groq and returns the answer.

    Args:
        prompt: the full Context + Question prompt (see prompts.py).
        temperature: low by default — factual/grounded answers should
                     be consistent, not creative.
        max_tokens: maximum length of the response.

    Returns:
        The model's text response as a string.
    """
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": GROUNDED_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content
