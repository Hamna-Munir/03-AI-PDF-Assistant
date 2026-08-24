# Day 15 — PDF Fundamentals & Text Extraction

**Objective:** Understand what a PDF actually is, and learn to extract usable text from one using Python.

---

## 📖 Theory

### What is a PDF?

PDF (Portable Document Format) is a file format designed to display content the same way on any device, regardless of software or hardware. Unlike a `.txt` or `.docx` file, a PDF doesn't store content as simple flowing text — it stores precise instructions for *where* each character, image, and shape should be drawn on the page. This is great for consistent visual appearance, but it makes extracting the underlying text more involved than just "opening the file."

### Text-based vs Scanned PDF

- **Text-based PDF** — the actual text characters are embedded in the file. This is what you get from a Word-to-PDF export, or a PDF generated directly from code. Text extraction works reliably on these.
- **Scanned PDF** — the "document" is really just an image (a photograph or scan) saved inside a PDF wrapper. There is no embedded text at all — to a text extractor, a scanned PDF looks empty. Getting text out of a scanned PDF requires OCR (Optical Character Recognition), which is a separate technique, not covered this week.

This distinction matters a lot for an AI PDF Assistant: it needs to detect when a PDF has no extractable text and tell the user, instead of silently failing or hallucinating an answer.

### PDF Text Extraction

Extracting text means walking through each page of a PDF and pulling out any embedded text content, page by page, into a plain string your Python program can work with.

### `pypdf`

`pypdf` is a Python library for reading and manipulating PDF files. It's the tool used this week for text extraction.

### `PdfReader`

`PdfReader` is the class in `pypdf` that opens a PDF file and gives you access to its contents (pages, metadata, etc.).

```python
from pypdf import PdfReader

reader = PdfReader("data/sample.pdf")
```

### `reader.pages`

Once a PDF is loaded into a `PdfReader`, `reader.pages` gives you a list-like collection of all the pages in the document — you can loop over it, or access a specific page by index (`reader.pages[0]` for the first page).

### `extract_text()`

Each page object has an `.extract_text()` method that returns the page's text content as a string. Looping over all pages and calling this on each one is how you build the full extracted text of a document.

```python
for page in reader.pages:
    print(page.extract_text())
```

---

## 📚 Reading

[pypdf documentation](https://pypdf.readthedocs.io/en/stable/) (official docs)

---

## 💻 Coding / Project Task

1. **Read a sample PDF** using `PdfReader`.
2. **Count total pages** in the document.
3. **Extract text from every page**, one page at a time.
4. **Print the extracted text** to the terminal to confirm it worked.

```python
from pypdf import PdfReader

reader = PdfReader("data/sample.pdf")

print(f"Total pages: {len(reader.pages)}")

for i, page in enumerate(reader.pages, start=1):
    text = page.extract_text()
    print(f"\n--- Page {i} ---")
    print(text)
```

---

## 🛠 Project Progress

```
PDF → Python → Extracted Text
```

The very first link in the pipeline is working: a PDF file can now be turned into plain text that later steps (chunking, context building) can work with.

---

## 🧠 Quiz

1. Why can't a PDF's text always be extracted the same way a `.txt` file's content can?
2. What's the difference between a text-based PDF and a scanned PDF?
3. Why would a scanned PDF return empty or missing text when run through `extract_text()`?
4. What does `reader.pages` represent in `pypdf`?
5. Why does the AI PDF Assistant need to know in advance whether extraction actually returned any text?

*(Try answering from memory first, then check the theory section above.)*

---

## 💡 Day 15 Takeaway

Before an AI can understand a document, it first needs that document's data extracted into a usable form. No amount of clever prompting can compensate for starting with empty or broken text.

---

## 🐞 Common Errors

| Error | Likely Cause | Fix |
|---|---|---|
| `extract_text()` returns an empty string | The PDF is scanned (image-based), not text-based | Detect empty extraction and inform the user OCR would be needed |
| `FileNotFoundError` when loading the PDF | Wrong file path, or PDF not in `data/` folder | Double-check the path is relative to where the script is run from |
| Extracted text looks jumbled or out of order | Some PDFs have unusual internal layout/column structures | Note this as a known limitation — not every PDF layout extracts cleanly |

---

## ✅ Checklist

- [ ] Understood what a PDF is and how it differs from plain text formats
- [ ] Understood text-based vs scanned PDFs
- [ ] Loaded a PDF with `PdfReader`
- [ ] Counted total pages
- [ ] Extracted text from every page
- [ ] Printed extracted text to the terminal
- [ ] Git commit made

---

## 📂 Git Commit

```bash
git commit -m "feat: add PDF text extraction with pypdf"
```
