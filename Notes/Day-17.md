# Day 17 — LLM + Document Context

**Objective:** Learn how to give an LLM external information (a document) so it can answer questions based on that information, instead of only its training data.

---

## 📖 Theory

### What is "context"?

In the context of LLMs, **context** means any information included in the prompt that the model can use to answer — beyond its own built-in training knowledge. A model doesn't automatically "know" what's inside a PDF someone uploaded a moment ago; the only way it can use that document is if the document's content (or relevant parts of it) is included directly in the prompt sent to it.

### System instructions (recap)

As covered in Week 2, system instructions set the AI's role, rules, and default behavior. In a document-Q&A assistant, the system instruction is where you tell the model *how* to treat the document context — for example, "only answer using the provided context."

### User instructions

The user instruction is the specific question being asked right now — e.g., "What is the main topic of this document?" On its own, this question means nothing to the model without the document context attached alongside it.

### Document context

Document context is the actual extracted text (or a relevant chunk of it) from the PDF, inserted into the prompt so the model has something concrete to answer from. Without it, the model can only guess or hallucinate an answer that sounds plausible but isn't grounded in the real document.

### The Context + Question prompt pattern

A reliable pattern for document Q&A prompts:

```
Context:
{document_text}

Question:
{user_question}

Answer the question using only the information in the context above.
```

This structure makes it explicit to the model which part is the source of truth (the context) and which part is the actual task (the question) — keeping the two clearly separated avoids the model confusing document content with instructions.

### Basic hallucination

Hallucination is when a model generates an answer that sounds confident and plausible but isn't actually supported by the real source material — essentially, the model "makes something up." Providing document context reduces this risk considerably, but doesn't eliminate it entirely; a model can still ignore the context and answer from its own training knowledge unless explicitly instructed not to (this gets addressed directly on Day 19).

---

## 📚 Reading

[OpenAI: Providing context in prompts](https://platform.openai.com/docs/guides/text-generation) (official docs)

---

## 💻 Coding / Project Task

Build the basic PDF Q&A flow:

```
PDF Text
    +
User Question
    ↓
Prompt
    ↓
LLM
    ↓
Answer
```

```python
def build_qa_prompt(document_text: str, question: str) -> str:
    return f"""Context:
{document_text}

Question:
{question}

Answer the question using only the information in the context above."""
```

Test it by letting the user ask something like:

> "Is PDF ka main topic kya hai?" (What is the main topic of this PDF?)

and confirming the answer actually reflects the uploaded document's content, not a generic response.

---

## 🛠 Project Progress

Basic PDF Q&A is now working — a user can upload a PDF and ask a question about its contents, and get an answer that's actually based on the document text extracted on Day 15–16.

---

## 🧠 Quiz

1. Why doesn't an LLM automatically "know" what's in a PDF the user just uploaded?
2. What's the difference between the "context" and the "question" in the Context + Question prompt pattern?
3. Why is it important to keep context and question clearly separated in the prompt, rather than blending them into one sentence?
4. What is hallucination, in one sentence?
5. Does providing document context completely eliminate hallucination risk? Why or why not?

*(Try answering from memory first, then check the theory section above.)*

---

## 💡 Day 17 Takeaway

An LLM doesn't automatically know a document's contents. Relevant document context has to be explicitly provided alongside the question — every single time — for the model to answer based on it.

---

## 🐞 Common Errors

| Error | Likely Cause | Fix |
|---|---|---|
| Answer sounds generic, not specific to the document | Document text wasn't actually included in the prompt sent to the model | Print the final prompt before sending it, and confirm the document text is really there |
| Answer contradicts the document | Model may be blending its own training knowledge with the context instead of relying on the context alone | Add a stronger instruction (see Day 19) explicitly restricting answers to the provided context |
| Prompt becomes too long / API error about context length | Very long PDF text pasted directly into the prompt without limiting size | This is exactly the problem Day 18 (chunking) solves |

---

## ✅ Checklist

- [ ] Understood what "context" means for an LLM
- [ ] Understood the difference between system and user instructions in this context
- [ ] Built the Context + Question prompt pattern
- [ ] Tested asking a real question about an uploaded PDF's content
- [ ] Confirmed the answer reflects the actual document, not a generic response
- [ ] Understood basic hallucination and why context reduces (but doesn't eliminate) it
- [ ] Git commit made

---

## 📂 Git Commit

```bash
git commit -m "feat: add basic PDF Q&A with document context"
```
