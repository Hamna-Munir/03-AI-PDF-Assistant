"""
chunking.py
Day 18 -> chunk_text(): splits large document text into overlapping chunks.
Day 18 -> select_relevant_chunks(): basic keyword-overlap context selection
           (a simple placeholder for embeddings-based retrieval, which
           comes later in Phase 2).
"""


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> list[str]:
    """
    Splits text into overlapping chunks.

    Args:
        text: the full extracted document text.
        chunk_size: max characters per chunk.
        overlap: characters shared between consecutive chunks.

    Returns:
        A list of text chunks.
    """
    if not text:
        return []

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


def select_relevant_chunks(chunks: list[str], question: str, top_n: int = 3) -> list[str]:
    """
    Day 18 — very basic context selection: scores each chunk by how many
    of the question's words appear in it, and returns the top N chunks.
    This is intentionally simple; embeddings-based retrieval is a Phase 2 topic.

    Args:
        chunks: list of text chunks from chunk_text().
        question: the user's question.
        top_n: how many top-scoring chunks to return.

    Returns:
        A list of the most relevant chunks, best match first.
    """
    if not chunks:
        return []

    question_words = set(w.lower() for w in question.split() if len(w) > 2)

    scored = []
    for chunk in chunks:
        chunk_lower = chunk.lower()
        score = sum(1 for word in question_words if word in chunk_lower)
        scored.append((score, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)

    # If nothing scored above 0, fall back to the first few chunks
    # rather than returning nothing.
    top_chunks = [chunk for score, chunk in scored[:top_n] if score > 0]
    if not top_chunks:
        top_chunks = chunks[:top_n]

    return top_chunks
