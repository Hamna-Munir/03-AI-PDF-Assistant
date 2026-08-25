# Day 16 — PDF Upload & File Handling

**Objective:** Let a user safely upload a PDF into the app, and process it — instead of only reading a hardcoded file from disk.

---

## 📖 Theory

### Streamlit file uploader

Streamlit provides a built-in widget, `st.file_uploader()`, that renders a drag-and-drop / browse box in the UI and returns the uploaded file as an in-memory object your code can work with directly — no need to manually save it to disk first.

```python
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
```

### File types

The `type` parameter restricts which file extensions the uploader will accept. Setting `type=["pdf"]` means the browser's file picker will only let the user select `.pdf` files in the first place — this is the first line of defense against wrong file types.

### Uploaded file objects

When a file is uploaded through Streamlit, `uploaded_file` is not a raw file path — it behaves like a file-like object (specifically, a `BytesIO`-style object) that libraries like `pypdf.PdfReader` can read directly, without saving anything to disk first:

```python
from pypdf import PdfReader

if uploaded_file is not None:
    reader = PdfReader(uploaded_file)
```

### File validation

Restricting the file picker to `.pdf` helps, but it doesn't guarantee the file is actually a valid, readable PDF (a renamed `.txt` file could still slip through in some cases, or the PDF could be corrupted). Real validation means trying to actually read the file and handling failure gracefully — not just trusting the extension.

### Basic user feedback

A good file-upload experience tells the user what happened at each step: confirmation the file was received, how many pages it has, and a short preview of what was extracted — rather than leaving them staring at a blank screen wondering if anything worked.

---

## 📚 Reading

[Streamlit file_uploader documentation](https://docs.streamlit.io/develop/api-reference/widgets/st.file_uploader) (official docs)

---

## 💻 Coding / Project Task

Build the PDF upload UI:

1. Add a file uploader restricted to PDF files only.
2. Show the uploaded file's name once received.
3. Show the total number of pages.
4. Show a short preview of the extracted text (e.g., first 500 characters).

```python
import streamlit as st
from pypdf import PdfReader

st.title("AI PDF Assistant")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None:
    st.write(f"**File name:** {uploaded_file.name}")

    reader = PdfReader(uploaded_file)
    st.write(f"**Total pages:** {len(reader.pages)}")

    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() or ""

    st.subheader("Text Preview")
    st.text(full_text[:500])
```

---

## 🛠 Project Progress

```
User
  ↓
Upload PDF
  ↓
Validate File
  ↓
Extract Text
  ↓
Show Preview
```

The assistant now has a real entry point — a user can upload their own PDF instead of the app only working on a hardcoded sample file.

---

## 🧠 Quiz

1. What does the `type` parameter of `st.file_uploader()` actually restrict?
2. Why can `pypdf.PdfReader` accept the uploaded file object directly, without saving it to disk first?
3. Why isn't restricting the file picker to `.pdf` enough validation on its own?
4. Name two pieces of feedback a user should see after a successful upload.
5. What should happen if `uploaded_file` is `None`?

*(Try answering from memory first, then check the theory section above.)*

---

## 💡 Day 16 Takeaway

Real AI applications don't just take text input — they have to handle different, sometimes messy, sources of user data (files, uploads, forms) safely and give the user clear feedback along the way.

---

## 🐞 Common Errors

| Error | Likely Cause | Fix |
|---|---|---|
| App crashes as soon as it loads, before any file is uploaded | Code tries to read `uploaded_file` before checking if it's `None` | Wrap PDF-reading logic in `if uploaded_file is not None:` |
| `extract_text()` returns `None` for some pages | Some pages genuinely have no extractable text | Use `page.extract_text() or ""` so `None` doesn't break string concatenation |
| Preview shows garbled or empty text | The PDF might be scanned/image-based (see Day 15) | Detect near-empty extraction and show a clear message instead of a blank preview |

---

## ✅ Checklist

- [ ] Understood how `st.file_uploader()` works
- [ ] Understood why uploaded files don't need to be saved to disk first
- [ ] Restricted uploads to PDF files only
- [ ] Displayed the uploaded file's name
- [ ] Displayed the total page count
- [ ] Displayed a text preview
- [ ] Git commit made

---

## 📂 Git Commit

```bash
git commit -m "feat: add PDF upload and file handling"
```
