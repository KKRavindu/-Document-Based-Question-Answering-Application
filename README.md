# 📄 DocuChat AI - Document-Based Question Answering Application

A sophisticated Python application that enables users to upload documents (PDF or TXT) and ask questions about their content using AI-powered natural language processing.

## 🎯 Project Overview

This application leverages Large Language Models (LLM) through OpenRouter API to provide accurate, context-aware answers to questions about uploaded documents. Built with Streamlit for an intuitive user experience.

## ✨ Features

- **📤 Document Upload**: Support for PDF and TXT file formats
- **🔍 Text Extraction**: Robust text processing from various document types
- **💬 Natural Q&A**: Ask questions in natural language and receive accurate answers
- **📊 Document Analytics**: Real-time statistics including character count, word count, and estimated pages
- **🎨 Modern UI**: Beautiful, responsive interface with gradient designs and smooth animations
- **💾 Chat History**: Track all your questions and answers in a conversation format
- **🔄 Real-time Processing**: Fast document processing and answer generation

## 🛠️ Technology Stack

- **Python 3.8+**
- **Streamlit**: Web application framework
- **PyPDF2**: PDF text extraction
- **OpenAI API**: LLM integration via OpenRouter
- **HTML/CSS**: Custom styling

## 📋 Prerequisites

Before running the application, ensure you have:

- Python 3.8 or higher installed
- pip (Python package manager)
- An OpenRouter API key ([Get one here](https://openrouter.ai/openai/gpt-oss-120b))

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/KKRavindu/-Document-Based-Question-Answering-Application
```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Key

Open `app.py` and replace the API key on line 18:

```python
OPENROUTER_API_KEY = "your-api-key-here"
```

Alternatively, use environment variables (recommended for production):

```bash
export OPENROUTER_API_KEY="your-api-key-here"
```

## 🎮 Usage

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Step-by-Step Guide

1. **Upload Document**: Click the file uploader in the sidebar and select a PDF or TXT file
2. **Process Document**: Click the "🚀 Process Document" button to extract text
3. **Ask Questions**: Type your question in the input field and click "🚀 Ask Question"
4. **View Answers**: See AI-generated answers based on your document content
5. **Review History**: Scroll through previous questions and answers
6. **Clear Data**: Use "🗑️ Clear Chat History" or "🗑️ Clear All" to reset

## 📁 Project Structure

```
docuchat-ai/
│
├── app.py                  # Main application file
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── .gitignore             # Git ignore file
├── LICENSE                # License information
├── USER_GUIDE.PDF         # PDF with usage instructions
└── images/                # Application screenshots
    ├── User Interface.png
    ├── upload doc.png
    ├── process doc.png
    └── Ask questions.png
```

## 🔧 Configuration

### API Settings

The application uses OpenRouter API with the following default settings:

- **Model**: `openai/gpt-oss-20b`
- **Max Tokens**: 1000
- **Temperature**: 0 (for factual responses)

You can modify these in the `get_answer_from_llm()` function in `app.py`.

### Supported File Types

- **PDF**: `.pdf` (all versions)
- **Text**: `.txt` (UTF-8 and Latin-1 encoding)

### File Size Limits

- Maximum upload size: 200MB (configurable in Streamlit settings)

## 🧪 Testing

### Manual Testing

1. Test with sample PDF document
2. Test with sample TXT document
3. Test with various question types
4. Test error handling with corrupted files

### Sample Questions to Try

- "What is the main topic of this document?"
- "Summarize the key points in this document"
- "What are the conclusions mentioned?"
- "List the important dates or numbers"

## 🐛 Troubleshooting

### Common Issues

**Issue**: API Error when generating answers
- **Solution**: Check your API key is valid and has sufficient credits

**Issue**: PDF extraction fails
- **Solution**: Ensure PDF is not password-protected or corrupted

**Issue**: Import errors
- **Solution**: Run `pip install -r requirements.txt` again

**Issue**: Port already in use
- **Solution**: Run `streamlit run app.py --server.port 8502`

## 📈 Performance Optimization

- For large documents (>50 pages), consider chunking the text
- Use caching with `@st.cache_data` for repeated operations
- Implement pagination for chat history with many questions

## 🔐 Security Considerations

- Never commit API keys to version control
- Use environment variables for sensitive data
- Sanitize user inputs before processing
- Implement rate limiting for API calls

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenRouter for providing LLM API access
- Streamlit for the amazing web framework
- PyPDF2 for PDF processing capabilities

**Built with ❤️ using Python, Streamlit, and AI**
