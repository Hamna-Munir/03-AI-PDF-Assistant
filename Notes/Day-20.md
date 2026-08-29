# Day 20 — Testing & Evaluation

**Objective:** Learn to systematically test an AI application against a real set of cases — normal, edge, and failure — instead of running one example and calling it "done."

---

## 📖 Theory

### AI application testing

Testing an AI application is different from testing regular software in one key way: the output isn't perfectly deterministic, so "does it work?" can't be answered by a single pass/fail run. It has to be answered by running the application against a *range* of realistic situations and checking whether it behaves acceptably across all of them — not just the one you happened to try first.

### Test cases

A test case is one specific scenario — a specific input and an expected kind of outcome — used to check whether the application behaves correctly. A good test suite for an AI PDF Assistant needs more than "ask it something and see if it answers."

### Normal cases

Normal cases are the everyday, expected usage patterns — a typical PDF, a reasonable question, an answer that should clearly be findable in the document. These confirm the basic pipeline (Day 15–19) works as designed.

### Edge cases

Edge cases are inputs at the boundary of what the application was designed to handle — not wrong, exactly, but unusual: a very short document, a very large one, an ambiguous question, a file that's technically valid but awkward. Edge cases reveal weaknesses that normal cases never would (this is exactly what happened with the prompt evaluation on Week 2, Day 13).

### Failure cases

Failure cases are inputs that should be explicitly rejected or handled gracefully — an unsupported file type, an empty PDF, a scanned PDF with no extractable text. The right behavior here isn't a crash or a hallucinated answer — it's a clear, honest message to the user about what went wrong.

### Evaluation criteria

For this week's testing, useful criteria include: does the app crash, does the answer correctly reflect the document, does the "I don't know" behavior (Day 19) trigger correctly when it should, and does the app give the user clear feedback instead of silent failure.

---

## 📚 Reading

[pytest documentation — writing test cases](https://docs.pytest.org/en/stable/getting-started.html) (official docs)

---

## 💻 Coding / Project Task

Write and run **at least 10 test cases**:

1. Normal question — answer clearly present in the document
2. Summary question — "What is this document about?"
3. Specific fact — a precise detail from the document
4. Question outside the PDF — should trigger the "I don't know" response (Day 19)
5. Empty PDF — a PDF with no pages or no text content
6. Scanned PDF — image-based, no extractable text (Day 15)
7. Very short PDF — a single sentence or a few words
8. Large PDF — tests that chunking (Day 18) actually kicks in and still produces a sensible answer
9. Ambiguous question — vague enough that a reasonable answer isn't obvious
10. Unsupported file — e.g., a `.docx` or `.txt` file uploaded despite the file-type restriction (Day 16)

For each test case, note: what was tested, what happened, and whether the result was acceptable.

---

## 🛠 Project Progress

The application has now been tested against both the happy path and a realistic set of failure conditions — not just "it worked when I tried it once."

---

## 🧠 Quiz

1. Why isn't a single successful test run enough to say an AI application "works"?
2. What's the difference between an edge case and a failure case?
3. Give an example of an edge case that could reveal a weakness a normal case wouldn't.
4. What should happen when an unsupported file type is uploaded — silently ignore it, crash, or something else?
5. Besides "did it answer correctly," what other criteria matter when evaluating an AI PDF Assistant's behavior?

*(Try answering from memory first, then check the theory section above.)*

---

## 💡 Day 20 Takeaway

AI applications need to be tested on failure cases just as much as the happy path. An assistant that works great on the obvious example but breaks on an empty PDF or a scanned document isn't actually reliable yet.

---

## 🐞 Common Errors

| Error | Likely Cause | Fix |
|---|---|---|
| App crashes on an empty/scanned PDF instead of showing a message | No check for empty extracted text before proceeding to Q&A | Add a check right after extraction: if text is empty/near-empty, show a clear message instead of continuing |
| Unsupported file type still gets processed | File-type restriction only applied at the UI level, not re-checked in code | Validate the file type/content again in code, not just via the uploader's `type` parameter |
| Large PDF test produces a vague or incomplete answer | Chunk selection isn't finding the actually relevant chunk(s) | Revisit the (basic) context selection logic from Day 18 for that specific test case |

---

## ✅ Checklist

- [ ] Understood the difference between normal, edge, and failure cases
- [ ] Wrote at least 10 test cases covering all 3 categories
- [ ] Ran all test cases and recorded what happened for each
- [ ] Confirmed the "I don't know" response triggers correctly (case 4)
- [ ] Confirmed empty/scanned PDFs are handled gracefully, not silently (cases 5–6)
- [ ] Confirmed unsupported files are rejected properly (case 10)
- [ ] Git commit made

---

## 📂 Git Commit

```bash
git commit -m "test: add 10 test cases covering normal, edge, and failure scenarios"
```
