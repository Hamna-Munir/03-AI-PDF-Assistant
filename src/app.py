"""
app.py
AI PDF Assistant — Streamlit UI
Developed by Hamna Munir

Homework.ai-inspired layout: light SaaS theme, left sidebar navigation
with working pages (PDF Assistant / Document History / Chunk Explorer),
chat-style bottom input bar for asking questions about the uploaded PDF.
"""

import sys
import os

# Streamlit Cloud runs this file with only its own directory (src/) on
# sys.path, not the repo root — so "from src.X import Y" fails there
# even though it works locally. Adding the repo root fixes it in both
# environments.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from src.pdf_reader import extract_text_from_pdf, is_pdf_readable
from src.chunking import chunk_text, select_relevant_chunks
from src.prompts import build_qa_prompt
from src.assistant import get_answer
from src.utils import format_preview, is_supported_file

st.set_page_config(page_title="AI PDF Assistant | Hamna Munir", page_icon="📄", layout="wide")

# ---------------------------------------------------------------------------
# Custom CSS — light SaaS theme (Homework.ai inspired)
# ---------------------------------------------------------------------------

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background: #f7f8fb; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container { padding-top: 1.6rem; max-width: 1100px; }

    /* Tighten default Streamlit vertical spacing between stacked elements */
    [data-testid="stVerticalBlock"] { gap: 0.35rem !important; }
    .element-container { margin-bottom: 0 !important; }
    div[data-testid="stExpander"] { margin: 0.3rem 0 !important; }
    div[data-testid="stExpander"] summary { padding: 0.5rem 0.8rem !important; min-height: unset !important; }

    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #eef0f4;
    }
    section[data-testid="stSidebar"] .block-container { padding-top: 1.5rem; }

    .sidebar-logo {
        display: flex;
        align-items: center;
        gap: 0.55rem;
        font-weight: 800;
        font-size: 1.05rem;
        color: #111827;
        margin-bottom: 1.4rem;
        padding: 0.5rem 0.6rem;
    }
    .sidebar-logo .logo-icon {
        width: 30px; height: 30px;
        background: linear-gradient(135deg, #3b82f6, #60a5fa);
        border-radius: 8px;
        display: flex; align-items: center; justify-content: center;
        color: white; font-size: 0.95rem;
        flex-shrink: 0;
    }
    .sidebar-logo .toggle-dot {
        margin-left: auto;
        width: 30px; height: 17px;
        background: #2563eb;
        border-radius: 999px;
        position: relative;
        flex-shrink: 0;
    }
    .sidebar-logo .toggle-dot::after {
        content: "";
        position: absolute;
        width: 12px; height: 12px;
        background: white;
        border-radius: 50%;
        top: 2.5px; right: 2.5px;
    }

    /* Sidebar nav buttons styled to look like the nav items */
    section[data-testid="stSidebar"] .stButton button {
        width: 100%;
        text-align: left;
        background: transparent;
        color: #4b5563;
        font-weight: 500;
        font-size: 0.92rem;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 0.8rem;
        margin-bottom: 0.15rem;
        box-shadow: none;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        background: #f3f4f6;
        color: #111827;
    }
    /* Active nav item — rendered as a static div (not a button) since
       current page doesn't need to be clickable, avoiding Streamlit's
       DOM nesting limitations with wrapping custom CSS around buttons */
    .nav-item.active-static {
        background: #eff4ff;
        color: #2563eb;
        font-weight: 600;
        font-size: 0.92rem;
        padding: 0.6rem 0.8rem;
        border-radius: 10px;
        margin-bottom: 0.15rem;
    }

    .topbar-title { font-size: 1.6rem; font-weight: 800; color: #111827; margin-bottom: 1.4rem; }
    .badge-pill {
        background: #fef3c7; color: #92400e; font-weight: 600; font-size: 0.82rem;
        padding: 0.35rem 0.9rem; border-radius: 999px; display: inline-block; margin-bottom: 0.8rem;
    }
    .hero-wrap { text-align: center; padding: 1.2rem 0 1.8rem 0; }
    .hero-title { font-size: 2.1rem; font-weight: 800; color: #111827; margin: 0.3rem 0; }
    .hero-title .accent { color: #2563eb; }
    .hero-subtitle { color: #6b7280; font-size: 1rem; max-width: 560px; margin: 0 auto; }

    .chat-card {
        background: #ffffff; border: 1px solid #eef0f4; border-radius: 20px;
        padding: 1.3rem 1.4rem; box-shadow: 0 4px 24px rgba(17,24,39,0.04);
    }
    .stFileUploader { padding: 0 !important; }
    .stFileUploader section {
        background: #f9fafc !important;
        border: 1.5px dashed #d7dbe3 !important;
        border-radius: 14px !important;
    }
    .stFileUploader section > div { color: #6b7280 !important; }
    .stFileUploader section small { color: #9ca3af !important; }
    .stFileUploader button {
        background: #2563eb !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    .stFileUploader button:hover { background: #1d4ed8 !important; }
    .upload-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #374151;
        margin-bottom: 0.4rem;
    }

    .info-strip { display: flex; gap: 1.6rem; color: #6b7280; font-size: 0.85rem; margin: 0.8rem 0 0.2rem 0; }
    .info-strip b { color: #111827; }

    .answer-card {
        background: #ffffff; border: 1px solid #eef0f4; border-left: 4px solid #2563eb;
        border-radius: 14px; padding: 1.3rem 1.5rem; margin-top: 1rem; color: #1f2937; line-height: 1.6;
    }
    .answer-label { font-size: 0.72rem; font-weight: 700; color: #2563eb; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 0.5rem; }

    .history-item {
        background: #ffffff; border: 1px solid #eef0f4; border-radius: 14px;
        padding: 1rem 1.2rem; margin-bottom: 0.8rem;
    }
    .history-q { font-weight: 700; color: #111827; margin-bottom: 0.4rem; }
    .history-a { color: #4b5563; font-size: 0.92rem; line-height: 1.55; }

    .chunk-item {
        background: #ffffff; border: 1px solid #eef0f4; border-radius: 12px;
        padding: 0.9rem 1.1rem; margin-bottom: 0.6rem; font-size: 0.85rem; color: #4b5563;
    }
    .chunk-index { font-weight: 700; color: #2563eb; font-size: 0.78rem; margin-bottom: 0.3rem; }

    .stTextInput input {
        background: #f9fafc !important; border: 1px solid #e5e7eb !important;
        border-radius: 12px !important; color: #111827 !important; padding: 0.7rem 1rem !important;
    }

    div[data-testid="column"] .stButton button,
    .chat-card .stButton button {
        background: #2563eb; color: white; font-weight: 600; border: none;
        border-radius: 10px; padding: 0.6rem 1.4rem; width: auto;
    }
    div[data-testid="column"] .stButton button:hover,
    .chat-card .stButton button:hover { background: #1d4ed8; }

    .app-footer {
        text-align: center; color: #9ca3af; font-size: 0.82rem; margin-top: 2.5rem;
        padding-top: 1.2rem; border-top: 1px solid #eef0f4;
    }
    .app-footer b { color: #2563eb; }

    /* Message composer bar (Homework.ai style) */
    .composer {
        background: #fbfbfd;
        border: 1px solid #eef0f4;
        border-radius: 20px;
        padding: 0.9rem 1.1rem 0.7rem 1.1rem;
        margin-top: 0.6rem;
    }
    .composer-icons {
        display: flex;
        justify-content: flex-end;
        gap: 0.9rem;
        color: #9ca3af;
        font-size: 1rem;
        margin-bottom: 0.6rem;
    }
    .composer-bottom-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-top: 0.5rem;
    }
    .composer-provider {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        background: #f3f4f6;
        border-radius: 10px;
        padding: 0.4rem 0.8rem;
        font-size: 0.82rem;
        color: #4b5563;
        font-weight: 500;
    }
    .composer .stTextInput input {
        background: transparent !important;
        border: none !important;
        padding: 0.2rem 0.1rem !important;
        font-size: 0.95rem !important;
    }
    .composer .stTextInput input::placeholder { color: #9ca3af; }
    .composer div[data-testid="column"] .stButton button {
        background: #2563eb;
        color: white;
        border-radius: 10px;
        width: 42px;
        height: 42px;
        padding: 0;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------

if "page" not in st.session_state:
    st.session_state.page = "home"
if "qa_history" not in st.session_state:
    st.session_state.qa_history = []
if "chunks" not in st.session_state:
    st.session_state.chunks = []
if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = None

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

with st.sidebar:
    st.markdown('''
    <div class="sidebar-logo">
        <div class="logo-icon">📄</div>
        <span>PDF Assist</span>
        <div class="toggle-dot"></div>
    </div>
    ''', unsafe_allow_html=True)

    nav_items = [
        ("home", "📄", "PDF Assistant"),
        ("history", "🕘", "Document History"),
        ("chunks", "🧩", "Chunk Explorer"),
    ]
    for key, icon, label in nav_items:
        if st.session_state.page == key:
            st.markdown(
                f'<div class="nav-item active-static">{icon}&nbsp;&nbsp;{label}</div>',
                unsafe_allow_html=True,
            )
        else:
            if st.button(f"{icon}  {label}", key=f"nav_{key}"):
                st.session_state.page = key
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#eff4ff; border-radius:14px; padding:1rem; font-size:0.82rem; color:#374151;">
        <b style="color:#2563eb;">Grounded Answers</b><br/>
        This assistant only answers from your uploaded document — and says so when it can't find something.
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# PAGE: Document History
# ---------------------------------------------------------------------------

if st.session_state.page == "history":
    st.markdown('<div class="topbar-title">🕘 Document History</div>', unsafe_allow_html=True)

    if not st.session_state.qa_history:
        st.info("No questions asked yet. Upload a PDF and ask something on the PDF Assistant page.")
    else:
        for entry in reversed(st.session_state.qa_history):
            st.markdown(f"""
            <div class="history-item">
                <div class="history-q">Q: {entry['question']}</div>
                <div class="history-a">{entry['answer']}</div>
            </div>
            """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# PAGE: Chunk Explorer
# ---------------------------------------------------------------------------

elif st.session_state.page == "chunks":
    st.markdown('<div class="topbar-title">🧩 Chunk Explorer</div>', unsafe_allow_html=True)

    if not st.session_state.chunks:
        st.info("No document loaded yet. Upload a PDF on the PDF Assistant page to see its chunks here.")
    else:
        st.caption(f"**{st.session_state.pdf_name}** was split into **{len(st.session_state.chunks)}** chunk(s).")
        for i, chunk in enumerate(st.session_state.chunks, start=1):
            st.markdown(f"""
            <div class="chunk-item">
                <div class="chunk-index">CHUNK {i} · {len(chunk)} chars</div>
                {format_preview(chunk, max_chars=200)}
            </div>
            """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# PAGE: PDF Assistant (home)
# ---------------------------------------------------------------------------

else:
    st.markdown('<div class="topbar-title">Welcome back, Hamna 👋</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="hero-wrap">
        <span class="badge-pill">✨ Week 03 · Document AI</span>
        <div class="hero-title">AI <span class="accent">PDF</span> Assistant</div>
        <div class="hero-subtitle">Upload any document and ask questions — answers are grounded strictly in what's on the page, not guesswork.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="chat-card">', unsafe_allow_html=True)

    st.markdown('<div class="upload-label">📎 Upload your document</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"], label_visibility="collapsed")

    if uploaded_file is not None:
        if not is_supported_file(uploaded_file.name):
            st.error("Unsupported file type. Please upload a PDF.")
            st.stop()

        with st.spinner("Extracting text..."):
            full_text, total_pages = extract_text_from_pdf(uploaded_file)

        st.markdown(f"""
        <div class="info-strip">
            <div>📄 <b>{uploaded_file.name}</b></div>
            <div>📑 <b>{total_pages}</b> pages</div>
        </div>
        """, unsafe_allow_html=True)

        if not is_pdf_readable(full_text):
            st.warning("This PDF doesn't appear to contain extractable text — it may be scanned/image-based.")
            st.stop()

        with st.expander("📖 Text Preview"):
            st.text(format_preview(full_text))

        # store chunks + name in session state so Chunk Explorer page can use them
        st.session_state.chunks = chunk_text(full_text, chunk_size=1000, overlap=100)
        st.session_state.pdf_name = uploaded_file.name

        st.markdown('<div class="composer">', unsafe_allow_html=True)
        st.markdown('<div class="composer-icons">↺ &nbsp; ↻ &nbsp; 🎙️ &nbsp; 📷 &nbsp; ✏️ &nbsp; 📎</div>', unsafe_allow_html=True)

        question = st.text_input(
            "Message",
            placeholder="Message on PDF Assist...",
            label_visibility="collapsed",
        )

        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.markdown('<div class="composer-provider">📄 &nbsp; Groq · Llama</div>', unsafe_allow_html=True)
        with col3:
            ask = st.button("➤", key="ask_btn")
        st.markdown('</div>', unsafe_allow_html=True)

        if ask and question.strip():
            with st.spinner("Thinking..."):
                relevant_chunks = select_relevant_chunks(st.session_state.chunks, question, top_n=3)
                context = "\n\n".join(relevant_chunks)
                prompt = build_qa_prompt(context, question)
                answer = get_answer(prompt)

            # save this Q&A into Document History
            st.session_state.qa_history.append({"question": question, "answer": answer})

            st.markdown(f"""
            <div class="answer-card">
                <div class="answer-label">Answer</div>
                {answer}
            </div>
            """, unsafe_allow_html=True)

    else:
        st.info("👆 Upload a PDF to start asking questions.")

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="app-footer">
    AI PDF Assistant · Week 3 of a 90-Day AI Engineering Roadmap · Developed by <b>Hamna Munir</b>
</div>
""", unsafe_allow_html=True)
