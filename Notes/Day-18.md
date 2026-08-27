# Day 18 — Text Chunking & Large Document Handling

**Objective:** Learn how to split a large document into manageable pieces, so it fits within an LLM's limits instead of being sent in one giant, unreliable block.

---

## 📖 Theory

### Context window

The **context window** is the maximum amount of text (measured in tokens) a model can process in a single request — this includes the system prompt, the user's question, and any context provided, combined. Every model has a fixed limit; there's no way to exceed it in one request.

### Token limits

As covered in Week 2 (Day 12), a token is roughly ¾ of a word on average. A large PDF — say, a 40-page report — could easily contain tens of thousands of tokens once fully extracted. Pasting all of that directly into a single prompt can exceed the context window, get expensive, or simply overwhelm the model with irrelevant text for a specific question.

### The large document problem

If a user asks a very specific question ("What's the refund policy in section 4?"), sending the *entire* document as context is wasteful and unreliable — the model has to search through a huge amount of irrelevant text to find the one relevant part, and it may lose track of details in a very long context. The fix isn't to send less accurately — it's to send *only the relevant part*.

### Text chunking

Chunking means splitting a large body of text into smaller, more manageable pieces (chunks) — usually a few hundred to a couple thousand characters each — so that only relevant chunks need to be sent to the model instead of the whole document.

### Chunk size

Chunk size is how large each piece of text is, usually measured in characters or tokens. Too small, and a chunk might cut off in the middle of important information. Too large, and you're back to the original problem of overwhelming the context window.

### Chunk overlap

Chunk overlap means letting consecutive chunks share a small amount of text at their boundary (e.g., the last 50 characters of chunk 1 are also the first 50 characters of chunk 2). This prevents a sentence or idea that happens to fall exactly on a chunk boundary from being split awkwardly and losing meaning in both pieces.

```
Chunk 1: [........................]
Chunk 2:                   [........................]
                            ^-- overlap region --^
```

### Basic context selection

Once a document is split into chunks, context selection is the (basic, for this week) process of deciding *which* chunk(s) to actually include in the prompt for a given question. This week, that selection can be simple (e.g., search chunks for keyword overlap with the question); more advanced selection using embeddings comes later, in Phase 2.

---

## 📚 Reading

[LangChain: Text Splitting Concepts](https://python.langchain.com/docs/concepts/text_splitters/) (conceptual reference — chunking strategy, not the LangChain library itself)

---

## 💻 Coding / Project Task

```
Large PDF
    ↓
Extracted Text
    ↓
Split into Chunks
    ↓
Chunks
```

```python
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
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks
```

Store the resulting chunks in a list and test with a real (longer) PDF — print each chunk's length and a short preview to confirm the splitting behaves as expected.

---

## 🛠 Project Progress

The foundation for handling large PDFs is now in place — documents no longer need to be sent to the model as one giant block of text.

---

## 🧠 Quiz

1. What is a context window, and why does it create a hard limit on how much text can be sent at once?
2. Why is sending an entire large document as context wasteful, even when it technically fits?
3. What problem does chunk overlap solve?
4. What's the tradeoff between chunk size being too small vs too large?
5. At this stage (Day 18), how is the assistant deciding which chunk(s) to use for a given question?

*(Try answering from memory first, then check the theory section above.)*

---

## 💡 Day 18 Takeaway

Sending an entire document to the LLM every time isn't a scalable or reliable approach. Breaking it into chunks — and eventually selecting only the relevant ones — is what makes large-document Q&A actually work.

---

## 🐞 Common Errors

| Error | Likely Cause | Fix |
|---|---|---|
| Last chunk is very short or empty | Loop doesn't stop cleanly at the end of the text | Confirm the `while start < len(text)` condition and check the final chunk manually |
| Chunks repeat too much text | `overlap` value is too close to (or larger than) `chunk_size` | Keep overlap meaningfully smaller than chunk size (e.g., 10% of it) |
| Important information split awkwardly across two chunks | Chunk size too small, or overlap too small for this document's structure | Increase chunk size or overlap and re-test |

---

## ✅ Checklist

- [ ] Understood context window and token limits
- [ ] Understood why sending a whole large document isn't scalable
- [ ] Understood chunk size and chunk overlap
- [ ] Built a `chunk_text()` function
- [ ] Tested chunking on a real (longer) PDF
- [ ] Stored and inspected the resulting chunks
- [ ] Git commit made

---

## 📂 Git Commit

```bash
git commit -m "feat: add text chunking for large PDF handling"
```
