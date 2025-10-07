"""
Document-Based Question Answering Application
Author: [Your Name]
Date: October 2025

This application allows users to upload PDF or TXT documents and ask questions
about their content using OpenRouter GPT-OSS-20B model.
"""

import streamlit as st
import PyPDF2
from io import BytesIO
import openai

# ============================================================
# CONFIGURATION - Add your OpenRouter API key here
# ============================================================
OPENROUTER_API_KEY = "add your API Key"  # Replace with your OpenRouter API key
openai.api_key = OPENROUTER_API_KEY
openai.api_base = "https://openrouter.ai/api/v1"

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Document Q&A Assistant",
    page_icon="📄",
    layout="wide"
)

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================
if 'document_text' not in st.session_state:
    st.session_state.document_text = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'document_name' not in st.session_state:
    st.session_state.document_name = None

# ============================================================
# DOCUMENT PROCESSING FUNCTIONS
# ============================================================
def extract_text_from_pdf(pdf_file):
    try:
        pdf_file.seek(0)
        pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_file.read()))
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip() if text.strip() else None
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return None

def extract_text_from_txt(txt_file):
    try:
        text = txt_file.read().decode('utf-8')
        return text.strip()
    except UnicodeDecodeError:
        txt_file.seek(0)
        try:
            text = txt_file.read().decode('latin-1')
            return text.strip()
        except Exception as e:
            st.error(f"Error reading text file: {e}")
            return None
    except Exception as e:
        st.error(f"Error reading text file: {e}")
        return None

# ============================================================
# AI QUESTION ANSWERING FUNCTION
# ============================================================
def get_answer_from_llm(question, document_text):
    prompt = f"""You are a helpful assistant answering questions based on the provided document content.

Document Content:
{document_text}

Question: {question}

Please provide a clear and accurate answer based solely on the information in the document. 
If the answer cannot be found in the document, please state that clearly."""

    try:
        response = openai.ChatCompletion.create(
            model="openai/gpt-oss-20b",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating answer: {e}"

# ============================================================
# MAIN USER INTERFACE
# ============================================================
st.title("📄 Document-Based Question Answering Assistant")
st.markdown("Upload a document (PDF or TXT) and ask questions about its content!")

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("📤 Upload Document")
    uploaded_file = st.file_uploader(
        "Choose a PDF or TXT file",
        type=['pdf', 'txt'],
        help="Upload a document to analyze (Max size: 200MB)"
    )

    if uploaded_file:
        st.info(f"**File:** {uploaded_file.name}")
        st.info(f"**Size:** {uploaded_file.size / 1024:.2f} KB")
        
        if st.button("📊 Process Document", use_container_width=True):
            with st.spinner("Processing document..."):
                if uploaded_file.type == "application/pdf":
                    text = extract_text_from_pdf(uploaded_file)
                else:
                    text = extract_text_from_txt(uploaded_file)
                
                if text:
                    st.session_state.document_text = text
                    st.session_state.document_name = uploaded_file.name
                    st.session_state.chat_history = []
                    st.success(f"✅ Document processed successfully!")
                    st.success(f"📝 Extracted {len(text)} characters")
                else:
                    st.error("❌ Failed to extract text from document.")

    if st.session_state.document_text:
        st.divider()
        st.header("📊 Document Statistics")
        char_count = len(st.session_state.document_text)
        word_count = len(st.session_state.document_text.split())
        line_count = len(st.session_state.document_text.split('\n'))
        st.metric("Document", st.session_state.document_name)
        st.metric("Characters", f"{char_count:,}")
        st.metric("Words", f"{word_count:,}")
        st.metric("Lines", f"{line_count:,}")
        
        if st.button("🗑️ Clear Document", use_container_width=True):
            st.session_state.document_text = None
            st.session_state.document_name = None
            st.session_state.chat_history = []
            st.rerun()

# ---------------- MAIN CONTENT ----------------
if st.session_state.document_text:
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("💬 Ask Questions")
        if st.session_state.chat_history:
            for i, (q, a) in enumerate(st.session_state.chat_history):
                st.markdown(f"**❓ Question {i+1}:** {q}")
                st.markdown(f"**💡 Answer:** {a}")
                st.divider()
        
        with st.form(key="question_form", clear_on_submit=True):
            question = st.text_input("Enter your question:", placeholder="What is this document about?")
            col_btn1, col_btn2 = st.columns([1, 5])
            with col_btn1:
                ask_button = st.form_submit_button("🚀 Ask")
            with col_btn2:
                clear_button = st.form_submit_button("🗑️ Clear History")
        
        if clear_button:
            st.session_state.chat_history = []
            st.rerun()
        
        if ask_button and question:
            with st.spinner("🤔 Thinking... Generating answer..."):
                answer = get_answer_from_llm(question, st.session_state.document_text)
                st.session_state.chat_history.append((question, answer))
                # ✅ DO NOT call st.rerun() here to avoid looping

    with col2:
        st.header("📖 Document Preview")
        preview_length = st.slider("Preview length (characters)", 100, 2000, 500, step=100)
        preview_text = st.session_state.document_text[:preview_length]
        if len(st.session_state.document_text) > preview_length:
            preview_text += "..."
        st.text_area("Content preview:", preview_text, height=400, disabled=True)
        if st.checkbox("Show full document"):
            st.text_area("Full document:", st.session_state.document_text, height=400, disabled=True)
else:
    st.info("👈 Please upload a document using the sidebar to get started!")

