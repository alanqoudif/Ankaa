"""
Utility functions for document preprocessing in the Legal AI Assistant.
"""

import os
import re
from typing import List, Dict, Any, Tuple
from langchain.schema import Document

def extract_document_metadata(file_path: str) -> Dict[str, Any]:
    """
    Extract metadata from document filename and path.
    
    Args:
        file_path: Path to the document file
        
    Returns:
        Dictionary with extracted metadata
    """
    filename = os.path.basename(file_path)
    base_name, _ = os.path.splitext(filename)
    
    # Try to extract document type, year, and number from filename
    # Assuming filenames might follow patterns like "RoyalDecree_15_2023.pdf" or "Law_Commercial_2018.pdf"
    metadata = {
        "source": file_path,
        "filename": filename,
        "base_name": base_name
    }
    
    # Extract document type (e.g., Law, Decree, Regulation)
    doc_type_match = re.search(r'(Law|Decree|Regulation|Act|Code|Order)', base_name, re.IGNORECASE)
    if doc_type_match:
        metadata["doc_type"] = doc_type_match.group(0)
    
    # Extract year if present (4-digit number)
    year_match = re.search(r'(19|20)\d{2}', base_name)
    if year_match:
        metadata["year"] = year_match.group(0)
    
    # Extract document number if present
    number_match = re.search(r'_(\d+)_', base_name)
    if number_match:
        metadata["number"] = number_match.group(1)
    
    return metadata

def clean_text(text: str) -> str:
    """
    Clean and normalize text from documents.
    
    Args:
        text: Text to clean
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Replace multiple newlines with a single newline
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Replace multiple spaces with a single space
    text = re.sub(r' {2,}', ' ', text)
    
    # Remove page numbers (common formats)
    text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
    
    # Remove header/footer markers
    text = re.sub(r'\n\s*-\s*\d+\s*-\s*\n', '\n', text)
    
    # Remove special characters that might interfere with processing
    text = re.sub(r'[^\w\s\.\,\;\:\(\)\[\]\{\}\"\'\-\–\—\؟\?\!\.\،\؛\:\"\'\)\(\]\[\}\{]', ' ', text)
    
    return text.strip()

def split_text_by_language(text: str) -> Tuple[str, str]:
    """
    Split text into Arabic and English components.
    
    Args:
        text: Text containing mixed languages
        
    Returns:
        Tuple of (arabic_text, english_text)
    """
    # Arabic Unicode range: \u0600-\u06FF
    arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]+[^a-zA-Z]*')
    english_pattern = re.compile(r'[a-zA-Z]+[^\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]*')
    
    arabic_parts = arabic_pattern.findall(text)
    english_parts = english_pattern.findall(text)
    
    arabic_text = ' '.join(arabic_parts).strip()
    english_text = ' '.join(english_parts).strip()
    
    return arabic_text, english_text

def detect_document_language(document: Document) -> str:
    """
    Detect the primary language of a document.
    
    Args:
        document: Document object
        
    Returns:
        Language code: 'ar' for Arabic, 'en' for English, 'mixed' for mixed content
    """
    text = document.page_content
    
    # Count Arabic and English characters
    arabic_chars = sum(1 for char in text if '\u0600' <= char <= '\u06FF' or '\u0750' <= char <= '\u077F' or '\u08A0' <= char <= '\u08FF')
    english_chars = sum(1 for char in text if 'a' <= char.lower() <= 'z')
    
    total_chars = len(text.strip())
    if total_chars == 0:
        return "unknown"
    
    arabic_ratio = arabic_chars / total_chars
    english_ratio = english_chars / total_chars
    
    if arabic_ratio > 0.6:
        return "ar"
    elif english_ratio > 0.6:
        return "en"
    else:
        return "mixed"

def group_documents_by_source(documents: List[Document]) -> Dict[str, List[Document]]:
    """
    Group documents by their source file.
    
    Args:
        documents: List of Document objects
        
    Returns:
        Dictionary mapping source paths to lists of documents
    """
    grouped = {}
    for doc in documents:
        source = doc.metadata.get("source", "unknown")
        if source not in grouped:
            grouped[source] = []
        grouped[source].append(doc)
    
    return grouped


if __name__ == "__main__":
    # Example usage
    sample_text = """
    المادة 279 من قانون العقوبات العماني
    يعاقب بالسجن مدة لا تقل عن ثلاثة أشهر ولا تزيد على ثلاث سنوات وبغرامة لا تقل عن مائة ريال عماني ولا تزيد على خمسمائة ريال عماني كل من ارتكب سرقة.
    
    Article 279 of the Omani Penal Code
    Whoever commits theft shall be punished with imprisonment for a period not less than three months and not exceeding three years, and a fine not less than 100 Omani Rials and not exceeding 500 Omani Rials.
    """
    
    cleaned = clean_text(sample_text)
    arabic, english = split_text_by_language(cleaned)
    
    print(f"Cleaned text:\n{cleaned}\n")
    print(f"Arabic text:\n{arabic}\n")
    print(f"English text:\n{english}\n")
    
    metadata = extract_document_metadata("/path/to/RoyalDecree_15_2023.pdf")
    print(f"Extracted metadata: {metadata}")
