"""
tests/test_chunking.py
Day 20 — tests for chunking.py.

Run with:
    pytest tests/test_chunking.py -v
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.chunking import chunk_text, select_relevant_chunks


def test_chunk_text_empty_input():
    assert chunk_text("") == []


def test_chunk_text_shorter_than_chunk_size():
    text = "Short text."
    chunks = chunk_text(text, chunk_size=1000, overlap=100)
    assert len(chunks) == 1
    assert chunks[0] == text


def test_chunk_text_splits_large_text():
    text = "A" * 2500
    chunks = chunk_text(text, chunk_size=1000, overlap=100)
    assert len(chunks) > 1
    # Every chunk should be at most chunk_size long
    assert all(len(c) <= 1000 for c in chunks)


def test_chunk_text_overlap_preserves_boundary_content():
    text = "0123456789" * 20  # 200 chars
    chunks = chunk_text(text, chunk_size=100, overlap=20)
    # The end of chunk 1 and start of chunk 2 should share the overlap region
    assert chunks[0][-20:] == chunks[1][:20]


def test_select_relevant_chunks_finds_keyword_match():
    chunks = [
        "This section discusses the company's refund policy in detail.",
        "This section discusses the shipping timeline for international orders.",
        "This section covers general terms and conditions.",
    ]
    question = "What is the refund policy?"
    result = select_relevant_chunks(chunks, question, top_n=1)
    assert "refund" in result[0].lower()


def test_select_relevant_chunks_falls_back_when_no_match():
    chunks = ["Alpha content here.", "Beta content here.", "Gamma content here."]
    question = "xyz nonexistent unrelated"
    result = select_relevant_chunks(chunks, question, top_n=2)
    # Should not return an empty list — falls back to first N chunks
    assert len(result) == 2


def test_select_relevant_chunks_empty_chunks_list():
    assert select_relevant_chunks([], "any question") == []
