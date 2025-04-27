# Sultanate Legal AI Assistant

## Level 1 - Smart Search Bot (Document QA)

This project implements a smart chatbot capable of searching and answering user questions based solely on Omani legal documents (in both Arabic and English).

### Features

- PDF document parsing and analysis
- Vector embeddings for efficient document retrieval
- Modern chat interface (using Streamlit)
- Local LLM for processing questions and answers
- Bilingual support (Arabic and English)

### Technical Stack

- Python 3.10+
- LangChain for document management
- ChromaDB for vector storage
- PyMuPDF for PDF parsing
- Streamlit for user interface
- Local LLM for inference

### Project Structure

```
.
├── README.md
├── requirements.txt
├── src
│   ├── data/              # Directory for legal documents
│   ├── utils/             # Utility functions
│   ├── models/            # LLM and embedding models
│   ├── ui/                # Streamlit UI components
│   ├── document_loader.py # PDF parsing functionality
│   ├── embeddings.py      # Document embedding generation
│   ├── retriever.py       # Vector search implementation
│   ├── llm_chain.py       # LLM chain for QA
│   └── app.py             # Main application entry point
```

### Setup and Installation

1. Clone the repository:
```bash
git clone git@github.com:alanqoudif/Ankaa.git
cd Ankaa
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run src/app.py
```

### Usage

1. Place your Omani legal documents (PDF format) in the `src/data/` directory
2. Run the application
3. Ask questions in either English or Arabic about Omani laws

### Example Questions

- "What is the punishment for theft according to Omani laws?"
- "ما هي عقوبة السرقة وفقًا للقوانين العمانية؟"
