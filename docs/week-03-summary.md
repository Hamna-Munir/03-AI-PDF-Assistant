# Engineering Journal — Week 03

Daily engineering log for the AI PDF Assistant (Days 15–21). Not a personal diary — a record of what was built, what broke, and what would be done differently.

---

## Day 15

**Today**
Learned how PDFs actually store content (layout instructions, not plain flowing text) and the difference between text-based and scanned PDFs. Built `extract_text_from_pdf()` using `pypdf.PdfReader`, looping over `reader.pages` and calling `.extract_text()` on each.

**Biggest Problem**
Understanding why a PDF can't just be "read like a text file" — it wasn't obvious at first why extraction needed a dedicated library instead of just opening the file.

**How I Solved It**
Read through how PDFs store content internally (drawing instructions vs a text stream) and confirmed with a real test PDF that `extract_text()` correctly reconstructs the visible text page by page.

**What I Would Improve**
Should test extraction against more than one PDF style (a plain text document vs one with columns/tables) to see how extraction quality varies — this week only used simple, straightforward PDFs.

---

## Day 16

**Today**
Added the Streamlit upload flow — `st.file_uploader()` restricted to PDFs, showing the file name, page count, and a text preview once a file is uploaded.

**Biggest Problem**
Making sure `PdfReader` could accept the Streamlit-uploaded file object directly, since it isn't a plain file path like the `data/sample.pdf` used in local testing on Day 15.

**How I Solved It**
Confirmed `pypdf.PdfReader` accepts file-like objects (which is what Streamlit's uploader returns) without needing to save the file to disk first — wrote `extract_text_from_pdf()` to accept either a path or a file-like object interchangeably.

**What I Would Improve**
Should add a check for `uploaded_file is None` more defensively at the very top of the script, rather than assuming the rest of the flow only runs after a successful upload.

---

## Day 17

**Today**
Built the Context + Question prompt pattern (`build_qa_prompt()`), and confirmed that including the actual PDF text in the prompt changes the model's answer from generic to document-specific.

**Biggest Problem**
Being tempted to blend the context and the question into one paragraph for a "more natural" prompt — but that made it harder to reason about what the model was actually using as source material.

**How I Solved It**
Kept context and question in clearly separate, labeled sections of the prompt (`Context:` / `Question:`), which made debugging easier and matched the pattern recommended in the day's reading.

**What I Would Improve**
At this stage, the entire extracted document text was still being sent as context for every question — which is exactly the scalability problem Day 18 exists to fix.

---

## Day 18

**Today**
Built `chunk_text()` with configurable chunk size and overlap, and `select_relevant_chunks()` for basic keyword-based context selection instead of sending the whole document every time.

**Biggest Problem**
Deciding how to handle the case where no chunk scores above zero for a given question — an early version of `select_relevant_chunks()` could have returned an empty list, leaving the assistant with no context at all.

**How I Solved It**
Added a fallback: if no chunk matches any keyword from the question, return the first N chunks instead of nothing. Verified with a test (`test_select_relevant_chunks_falls_back_when_no_match`) that this always returns something usable.

**What I Would Improve**
Keyword overlap is a genuinely weak selection method — a semantically relevant chunk that happens to use different wording than the question would be missed. This is a known, accepted limitation for this week, to be replaced by embeddings-based retrieval later.

---

## Day 19

**Today**
Added the grounding system prompt (`GROUNDED_SYSTEM_PROMPT`) with an explicit instruction to answer only from context and to respond with a specific "I could not find this information..." phrase when the context doesn't cover the question.

**Biggest Problem**
Making sure the "I don't know" phrasing was exact and consistent, rather than leaving the model free to phrase its uncertainty however it wanted — inconsistent phrasing would make it harder to detect this case programmatically later if needed.

**How I Solved It**
Specified the exact response text directly in the system prompt instead of a vague instruction like "say you don't know if you're not sure."

**What I Would Improve**
Haven't yet tested how the grounding instruction holds up when the relevant chunk exists but wasn't selected by Day 18's basic keyword matching — that's a different failure mode than the answer genuinely not being in the document, and it's worth testing separately.

---

## Day 20

**Today**
Wrote unit tests for `pdf_reader.py` and `chunking.py`, covering normal cases, edge cases (empty text, text shorter than chunk size, no keyword match), and planned the 10 manual test cases spanning normal, edge, and failure scenarios.

**Biggest Problem**
Deciding how to test PDF extraction without depending on a specific PDF file always being present in the repo (since PDF files can be large or awkward to commit).

**How I Solved It**
Used `pytest.mark.skipif` to skip the real-PDF test gracefully if `data/sample.pdf` isn't present, while keeping the rest of the test suite (which doesn't need a real file) always running.

**What I Would Improve**
Should record actual results for all 10 manual test cases directly in `notes/day-20.md` once run against the deployed app, the same way Week 2's Day 13 evaluation table was filled in with real output — a plan without recorded results is only half the exercise.

---

## Day 21

**Today**
Pulled everything together: reviewed error handling for empty/scanned PDFs and unsupported files, confirmed environment variables aren't hardcoded anywhere, and prepared the project for GitHub push and deployment.

**Biggest Problem**
Balancing "polish" against scope creep — it would be easy to keep adding features (multi-PDF support, page citations) instead of shipping what Week 3 actually set out to build.

**How I Solved It**
Used the Day 21 self-check questions as a hard boundary: if the core pipeline (upload → extract → chunk → grounded answer) works and fails gracefully on bad input, that's a legitimate v1.0 — extra features go in "Future Improvements," not into this week's scope.

**What I Would Improve**
Deployment and a fully screenshot-documented README are still pending as of this entry — worth treating "deployed and documented" as equally part of "done" as the code itself, not an afterthought tacked on at the very end.

---

## Week 03 — Overall Reflection

This week's real shift was learning that an LLM's "knowledge" of a document is entirely manufactured by the pipeline around it — extraction, chunking, and prompt construction all have to work correctly before grounding even becomes possible. And just like Week 2's Day 13 lesson, the instinct to trust something because it "should" work (a well-worded grounding instruction, a reasonable-looking chunk selection) isn't enough — it has to actually be tested against the cases that are likely to break it.
