# Day 21 — Polish, Deploy & Ship

**Objective:** Turn the finished Week 3 project into a portfolio-ready, deployed product — not just code that runs locally.

---

## 📖 Overview

This is the wrap-up day for Week 3. Nothing new is learned conceptually today — instead, everything from Day 15–20 gets polished, documented, tested end-to-end, and shipped as **AI PDF Assistant v1.0**.

### Final Pipeline

```
Local Project
      ↓
Testing
      ↓
GitHub
      ↓
Deployment
      ↓
Live AI PDF Assistant
```

---

## 📖 Theory

### Production-ready basics

A project being "done" locally isn't the same as it being production-ready. Production-ready means: it handles bad input without crashing, it doesn't expose secrets, and a stranger could run it from a fresh clone without guessing missing steps.

### UI polish

UI polish means the difference between "it technically works" and "it's pleasant and clear to use" — consistent spacing, clear labels, visible feedback (spinners, success/error messages), and no dead ends where the user doesn't know what happened.

### Deployment basics

Deployment means making the app accessible via a URL, not just `localhost`. For a Streamlit app, this typically means pushing to GitHub and connecting the repo to Streamlit Community Cloud (or a similar host), which builds and serves the app from the repository.

### Environment variables

Secrets (like API keys) should never be committed to GitHub. Locally, they live in `.env` (excluded via `.gitignore`). When deploying, the hosting platform provides its own secrets/environment variable settings — the deployed app reads keys from there instead of from a local `.env` file.

### README writing

The README is often the very first thing anyone — a recruiter, a hiring manager, another developer — reads about a project. It should let a stranger understand what the project does, see it working (screenshots or a live link), and get it running themselves within a few minutes.

### Project documentation

Beyond the README, documentation includes the week summary (`docs/week-03-summary.md`) and the engineering journal (`journal.md`) — these show *how* the project was built and what was learned, which matters for a learning portfolio specifically.

---

## 💻 Final Project Tasks

- [ ] **UI polish** — clean labels, spinners, clear error/warning messages
- [ ] **Upload flow test** — confirm PDF upload → extraction → chunking works end-to-end
- [ ] **PDF Q&A test** — confirm grounded answers work correctly, including the "I don't know" case
- [ ] **Error handling** — empty PDFs, scanned PDFs, unsupported files all handled gracefully (Day 20)
- [ ] **Clean code** — remove leftover debug prints, unused imports, dead code
- [ ] **`.env.example`** — confirm it's accurate and doesn't contain a real key
- [ ] **`requirements.txt`** — confirm it lists every package actually used
- [ ] **README** — updated with final features, install steps, and usage examples
- [ ] **Screenshots** — at least one showing a successful upload + grounded answer
- [ ] **GitHub push** — all Day 15–21 work committed
- [ ] **Streamlit deployment** — app live at a public URL

---

## 🧠 Self-Check Before Shipping

1. Does the app handle an empty or scanned PDF without crashing?
2. Does asking a question outside the document's scope reliably trigger the "I don't know" response?
3. Is the API key read from environment variables only — never hardcoded anywhere in the code?
4. Would a stranger be able to clone this repo, follow the README, and get it running in under 5 minutes?
5. Is the deployed (not just local) version actually working end-to-end?

If any answer is "no," that's today's real to-do list.

---

## 📂 Week 3 Repository — Final Structure

```
03-AI-PDF-Assistant/
│
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── .env.example
│
├── docs/
│   └── week-03-summary.md
│
├── notes/
│   ├── day-15.md
│   ├── day-16.md
│   ├── day-17.md
│   ├── day-18.md
│   ├── day-19.md
│   ├── day-20.md
│   └── day-21.md
│
├── assets/
│   ├── banner.svg
│   └── screenshots/
│
├── data/
│   └── sample.pdf
│
├── tests/
│   ├── test_pdf_reader.py
│   └── test_chunking.py
│
├── src/
│   ├── __init__.py
│   ├── app.py
│   ├── config.py
│   ├── pdf_reader.py
│   ├── chunking.py
│   ├── prompts.py
│   ├── assistant.py
│   └── utils.py
│
└── journal.md
```

---

## 📂 Git Commit

```bash
git add .
git commit -m "release: ship AI PDF assistant v1.0"
git push
```

---

## 🎯 Next Week Preview

Week 3 completes Phase 1's document-AI stretch. Check the roadmap for the Week 4 repository name and topics once ready — Phase 1 continues to build toward the final Foundation project before Phase 2 (Agent Engineering) begins.
