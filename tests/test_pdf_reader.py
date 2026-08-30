"""
tests/test_pdf_reader.py
Day 20 — tests for pdf_reader.py.

Run with:
    pytest tests/test_pdf_reader.py -v

Note: test_extract_text_from_real_pdf requires a valid PDF at
data/sample.pdf. If that file isn't present, that specific test
will be skipped.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from src.pdf_reader import is_pdf_readable, extract_text_from_pdf


def test_is_pdf_readable_true_for_normal_text():
    text = "This is a perfectly normal amount of extracted text from a PDF."
    assert is_pdf_readable(text) is True


def test_is_pdf_readable_false_for_empty_text():
    assert is_pdf_readable("") is False


def test_is_pdf_readable_false_for_near_empty_text():
    # Simulates a scanned PDF that extracted almost nothing
    assert is_pdf_readable("   \n  ") is False


def test_is_pdf_readable_respects_min_chars():
    short_text = "Hi"
    assert is_pdf_readable(short_text, min_chars=20) is False
    assert is_pdf_readable(short_text, min_chars=1) is True


@pytest.mark.skipif(
    not os.path.exists(os.path.join(os.path.dirname(__file__), "..", "data", "sample.pdf")),
    reason="data/sample.pdf not present",
)
def test_extract_text_from_real_pdf():
    sample_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample.pdf")
    text, pages = extract_text_from_pdf(sample_path)
    assert pages >= 1
    assert isinstance(text, str)
