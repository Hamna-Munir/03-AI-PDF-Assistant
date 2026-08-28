# Day 19 — Grounded & Reliable AI Responses

**Objective:** Learn how to keep the AI's answers strictly inside the boundaries of the provided document — and make it say "I don't know" instead of guessing.

---

## 📖 Theory

### Hallucination (recap + deeper look)

Day 17 introduced hallucination as an AI generating a confident-sounding answer that isn't actually supported by the source material. The risk doesn't disappear just because document context is provided — a model can still blend its own training knowledge with the context, or fill gaps with a plausible-sounding guess, unless it's explicitly told not to.

### Grounding

**Grounding** means constraining the model's answer to only the information actually present in the given context — nothing from its general training knowledge, and nothing invented to fill a gap. A grounded answer can always be traced back to a specific part of the source document.

### Context boundaries

Context boundaries are the explicit limits placed on what the model is allowed to use when answering: only the text provided in this request, nothing else. Without stating this boundary directly, the model has no way of knowing it *shouldn't* fall back on its general knowledge when the context doesn't have the answer.

### "Answer only from the document"

This is the core instruction that enforces grounding. Stating it explicitly — not implying it — is what actually changes model behavior:

```
Answer only from the provided PDF context.
If the answer is not present, say that you could not find it in the document.
```

### "I don't know" responses

Teaching the model to say "I don't know" (in a specific, consistent phrasing) when the document doesn't contain the answer is a deliberate reliability feature, not a failure state. A model that always tries to produce *some* answer, even when it has no real basis for one, is far more likely to hallucinate.

### Basic prompt constraints

Constraints are explicit rules embedded in the prompt that shape what the model is and isn't allowed to do. For grounding specifically, the key constraints are: (1) use only the provided context, and (2) explicitly decline to answer when the context doesn't cover the question.

---

## 📚 Reading

[OpenAI: Reducing hallucinations](https://platform.openai.com/docs/guides/prompt-engineering) (official docs — see grounding/context-related guidance)

---

## 💻 Coding / Project Task

Update the assistant's system instruction to enforce grounding:

```python
GROUNDED_SYSTEM_PROMPT = (
    "You are a document assistant. Answer only from the provided PDF "
    "context. If the answer is not present in the context, say: "
    "'I could not find this information in the provided document.' "
    "Do not use outside knowledge, and do not guess."
)
```

**Test case:**

Ask a question whose answer is *not* in the PDF, for example:

> "What is the CEO's name?" (when the document never mentions a CEO)

**Expected output:**

> "I could not find this information in the provided document."

If the model instead invents a plausible-sounding name, the grounding instruction needs to be strengthened or moved earlier/more prominently in the prompt.

---

## 🛠 Project Progress

Hallucination-reduction behavior has been added — the assistant now distinguishes between "the answer is in the document" and "the answer is not in the document," instead of always producing *some* answer regardless of whether it's actually supported.

---

## 🧠 Quiz

1. What does "grounding" mean for an AI's answer?
2. Why is stating context boundaries explicitly necessary, rather than assuming the model will infer them?
3. Write the exact phrase the assistant should return when the answer isn't in the document.
4. Why is a model saying "I don't know" sometimes *more* reliable than a model that always answers something?
5. What test would you run to confirm grounding is actually working, rather than just assuming it is?

*(Try answering from memory first, then check the theory section above.)*

---

## 💡 Day 19 Takeaway

Reliable AI doesn't mean answering every question — it means knowing when to say "I don't know." That's a form of reliability just as important as giving a correct answer.

---

## 🐞 Common Errors

| Error | Likely Cause | Fix |
|---|---|---|
| Model still answers questions not covered by the document | Grounding instruction too soft, or buried among other instructions | Make the constraint explicit and place it clearly in the system prompt |
| Model refuses to answer even when the information IS in the document | Instruction is too strict, or the relevant chunk wasn't actually included in context | Confirm the correct chunk was selected/included before blaming the instruction |
| "I don't know" phrasing is inconsistent between requests | No exact phrase specified in the instruction | Give the model the exact wording to use, rather than a vague "say you don't know" |

---

## ✅ Checklist

- [ ] Understood grounding and context boundaries
- [ ] Understood why "I don't know" is a reliability feature, not a failure
- [ ] Updated the system prompt to enforce "answer only from the document"
- [ ] Tested with a question NOT covered by the PDF
- [ ] Confirmed the assistant responded with the correct "not found" message
- [ ] Git commit made

---

## 📂 Git Commit

```bash
git commit -m "feat: add grounding constraints to reduce hallucination"
```
