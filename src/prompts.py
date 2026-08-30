"""
prompts.py
Day 17 -> build_qa_prompt(): Context + Question prompt pattern.
Day 19 -> GROUNDED_SYSTEM_PROMPT: enforces "answer only from the document".
"""

GROUNDED_SYSTEM_PROMPT = (
    "You are a document assistant. Answer only from the provided PDF "
    "context. If the answer is not present in the context, respond "
    "exactly with: 'I could not find this information in the provided "
    "document.' Do not use outside knowledge, and do not guess."
)


def build_qa_prompt(context: str, question: str) -> str:
    """
    Day 17 — Context + Question prompt pattern.
    Keeps context and question clearly separated so the model doesn't
    confuse document content with instructions.

    Args:
        context: relevant document text (full text or selected chunks).
        question: the user's question.

    Returns:
        The full prompt string to send to the LLM.
    """
    return f"""Context:
{context}

Question:
{question}

Answer the question using only the information in the context above."""
