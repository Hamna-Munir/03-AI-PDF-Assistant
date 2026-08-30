"""
pdf_reader.py
Day 15 -> extract_text_from_pdf(): reads a PDF and pulls out its text.
Day 16 -> handles Streamlit-uploaded file objects directly (no disk save needed).
Day 20 -> is_pdf_readable() detects empty/scanned PDFs for graceful failure handling.
"""

from pypdf import PdfReader


def extract_text_from_pdf(file) -> tuple[str, int]:
    """
    Extracts all text from a PDF.

    Args:
        file: a file path (str) OR a file-like object (e.g. from
              st.file_uploader) that pypdf.PdfReader can accept directly.

    Returns:
        A tuple of (full_extracted_text, total_pages).
    """
    reader = PdfReader(file)
    total_pages = len(reader.pages)

    full_text = ""
    for page in reader.pages:
        page_text = page.extract_text() or ""
        full_text += page_text + "\n"

    return full_text.strip(), total_pages


def is_pdf_readable(extracted_text: str, min_chars: int = 20) -> bool:
    """
    Day 20 — basic check to catch empty or scanned (image-only) PDFs
    before proceeding to Q&A, instead of silently failing later.

    Args:
        extracted_text: the text returned by extract_text_from_pdf().
        min_chars: minimum character count to consider the PDF "readable".

    Returns:
        True if the PDF appears to have usable extracted text.
    """
    return len(extracted_text.strip()) >= min_chars
