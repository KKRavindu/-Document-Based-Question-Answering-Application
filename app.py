"""
This application allows users to upload PDF or TXT documents and ask questions
about their content using OpenRouter GPT-OSS-20B model.
"""

import streamlit as st
import PyPDF2
from io import BytesIO
import openai

# ============================================================
# CONFIGURATION
# ============================================================
# Set up OpenRouter API credentials for accessing the GPT model
OPENROUTER_API_KEY = "add your API key here"
openai.api_key = OPENROUTER_API_KEY
openai.api_base = "https://openrouter.ai/api/v1"

# ============================================================
# PAGE CONFIGURATION
# ============================================================
# Configure the Streamlit page settings
st.set_page_config(
    page_title="DocuChat AI - Document Q&A Assistant",
    page_icon="🤖",
    layout="wide",  # Use wide layout for better space utilization
    initial_sidebar_state="expanded"  # Show sidebar by default
)

# ============================================================
# CUSTOM CSS FOR MODERN DESIGN
# ============================================================
# Inject custom CSS to style the application with modern design elements
st.markdown("""
    <style>
    /* Main theme colors - CSS variables for consistent color scheme */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #8b5cf6;
        --accent-color: #ec4899;
        --success-color: #10b981;
        --warning-color: #f59e0b;
    }
    
    /* Hide Streamlit branding elements for cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom header styling with gradient background */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    /* Main header title styling */
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        margin: 0;
        font-weight: 700;
    }
    
    /* Header subtitle styling */
    .main-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    /* Base styling for all chat messages */
    .chat-message {
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        animation: slideIn 0.3s ease-out;  /* Add smooth entrance animation */
    }
    
    /* Dark styling for question boxes with blue accent */
    .question-box {
            background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
            border-left: 4px solid #3b82f6;
    }
    
    /* Dark styling for answer boxes with blue accent */
    .answer-box {
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        border-left: 4px solid #3b82f6;
    }
    
    /* Chat message heading styling */
    .chat-message h4 {
        color: white;
        margin: 0 0 0.5rem 0;
        font-weight: 600;
    }
    
    /* Chat message text content styling */
    .chat-message p {
        color: white;
        margin: 0;
        line-height: 1.6;
    }
    
    /* Slide-in animation for chat messages */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Stat card styling for metrics and features */
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
        margin-bottom: 1rem;
    }
    
    /* Stat card number/icon styling */
    .stat-card h3 {
        color: white;
        font-size: 2rem;
        margin: 0;
        font-weight: 700;
    }
    
    /* Stat card label styling */
    .stat-card p {
        color: rgba(255, 255, 255, 0.8);
        margin: 0.5rem 0 0 0;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Upload section styling (currently not used but available) */
    .upload-section {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .upload-section h3 {
        color: white;
        margin-bottom: 1rem;
    }
    
    /* Info boxes for displaying file information in sidebar */
    .info-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 8px;
        color: white;
        margin: 1rem 0;
    }
    
    /* Custom button styling with gradient and hover effects */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    /* Button hover effect - lift and shadow */
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Empty state styling when no document is loaded */
    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 15px;
        color: white;
    }
    
    /* Empty state icon/emoji styling */
    .empty-state h2 {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    /* Empty state text styling */
    .empty-state p {
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    /* Preview box styling for document content display */
    .preview-box {
        background: #f8f9fa;
        border: 2px solid #e9ecef;
        border-radius: 8px;
        padding: 1rem;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================
# Initialize session state variables to persist data across reruns
if 'document_text' not in st.session_state:
    st.session_state.document_text = None  # Stores the extracted document text
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []  # Stores question-answer pairs
if 'document_name' not in st.session_state:
    st.session_state.document_name = None  # Stores the uploaded file name

# ============================================================
# DOCUMENT PROCESSING FUNCTIONS
# ============================================================
def extract_text_from_pdf(pdf_file):
    """
    Extract text content from a PDF file.
    
    Args:
        pdf_file: Uploaded PDF file object
        
    Returns:
        str: Extracted text from all pages or None if extraction fails
    """
    try:
        pdf_file.seek(0)  # Reset file pointer to beginning
        pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_file.read()))
        text = ""
        # Loop through all pages and extract text
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip() if text.strip() else None
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return None

def extract_text_from_txt(txt_file):
    """
    Extract text content from a TXT file with encoding fallback.
    
    Args:
        txt_file: Uploaded TXT file object
        
    Returns:
        str: Extracted text or None if extraction fails
    """
    try:
        # Try UTF-8 encoding first (most common)
        text = txt_file.read().decode('utf-8')
        return text.strip()
    except UnicodeDecodeError:
        # Fallback to latin-1 encoding if UTF-8 fails
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
    """
    Generate an answer to the user's question using OpenRouter GPT model.
    
    Args:
        question (str): User's question about the document
        document_text (str): Full text content of the document
        
    Returns:
        str: AI-generated answer or error message
    """
    # Create a prompt that includes the document content and question
    prompt = f"""You are a helpful assistant answering questions based on the provided document content.

Document Content:
{document_text}

Question: {question}

Please provide a clear and accurate answer based solely on the information in the document. 
If the answer cannot be found in the document, please state that clearly."""

    try:
        # Call OpenRouter API to generate answer
        response = openai.ChatCompletion.create(
            model="openai/gpt-oss-20b",  # Specify the model to use
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,  # Limit response length
            temperature=0  # Set to 0 for more deterministic/factual responses
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating answer: {e}"

# ============================================================
# MAIN USER INTERFACE
# ============================================================

# Display custom header with branding
st.markdown("""
    <div class="main-header">
        <h1>🤖 DocuChat AI</h1>
        <p>Your Intelligent Document Assistant - Upload, Ask, and Discover!</p>
    </div>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("### 📤 Upload Your Document")
    st.markdown("---")
    
    # File uploader widget for PDF and TXT files
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['pdf', 'txt'],  # Only accept PDF and TXT files
        help="Supported formats: PDF, TXT (Max: 200MB)",
        label_visibility="collapsed"  # Hide the default label
    )

    # Display file information if a file is uploaded
    if uploaded_file:
        st.markdown(f"""
            <div class="info-box">
                <strong>📄 {uploaded_file.name}</strong><br>
                📊 Size: {uploaded_file.size / 1024:.2f} KB
            </div>
        """, unsafe_allow_html=True)
        
        # Button to process the uploaded document
        if st.button("🚀 Process Document", use_container_width=True, type="primary"):
            with st.spinner("🔄 Processing your document..."):
                # Extract text based on file type
                if uploaded_file.type == "application/pdf":
                    text = extract_text_from_pdf(uploaded_file)
                else:
                    text = extract_text_from_txt(uploaded_file)
                
                # Store extracted text in session state if successful
                if text:
                    st.session_state.document_text = text
                    st.session_state.document_name = uploaded_file.name
                    st.session_state.chat_history = []  # Clear previous chat history
                    st.success("✅ Document processed successfully!")
                    st.balloons()  # Show celebration animation
                else:
                    st.error("❌ Failed to extract text from document.")

    # Display document statistics if a document is loaded
    if st.session_state.document_text:
        st.markdown("---")
        st.markdown("### 📊 Document Insights")
        
        # Calculate document statistics
        char_count = len(st.session_state.document_text)
        word_count = len(st.session_state.document_text.split())
        line_count = len(st.session_state.document_text.split('\n'))
        
        # Display metrics in two columns
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📝 Characters", f"{char_count:,}")
            st.metric("📄 Lines", f"{line_count:,}")
        with col2:
            st.metric("💬 Words", f"{word_count:,}")
            st.metric("📖 Pages", f"~{word_count // 250}")  # Estimate pages (250 words/page)
        
        st.markdown("---")
        # Button to clear all data and start fresh
        if st.button("🗑️ Clear All", use_container_width=True, type="secondary"):
            st.session_state.document_text = None
            st.session_state.document_name = None
            st.session_state.chat_history = []
            st.rerun()  # Refresh the app

# ---------------- MAIN CONTENT ----------------
if st.session_state.document_text:
    # Question Input Section
    st.markdown("### 💬 Ask Questions About Your Document")
    
    # Create layout with question input and ask button
    col1, col2 = st.columns([3, 1])
    with col1:
        question = st.text_input(
            "Your question:",
            placeholder="e.g., What is the main topic of this document?",
            label_visibility="collapsed"
        )
    with col2:
        ask_button = st.button("🚀 Ask Question", use_container_width=True, type="primary")
    
    # Button to clear chat history
    col3, col4 = st.columns([1, 1])
    with col3:
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    # Process question when ask button is clicked
    if ask_button and question:
        with st.spinner("🤔 AI is thinking..."):
            answer = get_answer_from_llm(question, st.session_state.document_text)
            # Add question-answer pair to chat history
            st.session_state.chat_history.append((question, answer))
    
    st.markdown("---")
    
    # Display chat history in reverse order (newest first)
    if st.session_state.chat_history:
        st.markdown("### 📜 Conversation History")
        for i, (q, a) in enumerate(reversed(st.session_state.chat_history)):
            # Display question box
            st.markdown(f"""
                <div class="chat-message question-box">
                    <h4>❓ Question {len(st.session_state.chat_history) - i}</h4>
                    <p>{q}</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Display answer box
            st.markdown(f"""
                <div class="chat-message answer-box">
                    <h4>💡 Answer</h4>
                    <p>{a}</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("💭 No questions asked yet. Start by typing your question above!")
    
    # Document Preview Section (collapsible)
    with st.expander("📖 View Document Preview", expanded=False):
        # Slider to control preview length
        preview_length = st.slider("Preview length (characters)", 100, 2000, 500, step=100)
        preview_text = st.session_state.document_text[:preview_length]
        if len(st.session_state.document_text) > preview_length:
            preview_text += "..."
        st.text_area("Document content:", preview_text, height=300, disabled=True)
        
        # Checkbox to show full document
        if st.checkbox("Show full document"):
            st.text_area("Full document:", st.session_state.document_text, height=500, disabled=True)

else:
    # Empty State - shown when no document is loaded
    st.markdown("""
        <div class="empty-state">
            <h2>📄</h2>
            <p><strong>Welcome to DocuChat AI!</strong></p>
            <p>Upload a document from the sidebar to start asking questions</p>
            <p>Supported formats: PDF and TXT files</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Feature highlights - display key features in three columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div class="stat-card">
                <h3>🚀</h3>
                <p>Fast Processing</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="stat-card">
                <h3>🤖</h3>
                <p>AI-Powered</p>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class="stat-card">
                <h3>💬</h3>
                <p>Natural Conversations</p>
            </div>
        """, unsafe_allow_html=True)

# Footer section
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem 0;">
        <p>Built with ❤️ using Streamlit and OpenRouter AI</p>
    </div>
""", unsafe_allow_html=True)
