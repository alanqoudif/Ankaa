"""
Document loader for parsing PDF files of Omani legal documents.
Supports both Arabic and English documents.
"""

import os
try:
    import fitz  # PyMuPDF
except ImportError:
    raise ImportError(
        "Could not import the PyMuPDF library (imported as 'fitz'). "
        "Please make sure PyMuPDF is installed correctly by running: "
        "pip install pymupdf==1.23.7"
    )
import re
from typing import List, Dict, Optional, Tuple, Any
from langchain.schema import Document
from tqdm import tqdm
from document_structure import DocumentStructureAnalyzer

class LegalDocumentLoader:
    """Loader for Omani legal documents in PDF format."""
    
    def __init__(self, directory_path: str):
        """
        Initialize the document loader.
        
        Args:
            directory_path: Path to the directory containing PDF documents
        """
        self.directory_path = directory_path
        self.structure_analyzer = DocumentStructureAnalyzer()
        
    def _extract_metadata(self, pdf_document, file_path: str) -> Dict:
        """Extract metadata from PDF document."""
        metadata = pdf_document.metadata
        result = {
            "title": metadata.get("title", "") if metadata else "",
            "author": metadata.get("author", "") if metadata else "",
            "subject": metadata.get("subject", "") if metadata else "",
            "creator": metadata.get("creator", "") if metadata else "",
            "producer": metadata.get("producer", "") if metadata else "",
            "creation_date": metadata.get("creationDate", "") if metadata else "",
            "modification_date": metadata.get("modDate", "") if metadata else "",
            "page_count": pdf_document.page_count,
            "source": file_path,
            "filename": os.path.basename(file_path)
        }
        
        # Try to extract law name from filename or title
        law_name = self._extract_law_name(file_path, result["title"])
        if law_name:
            result["law_name"] = law_name
            
        return result
        
    def _extract_law_name(self, file_path: str, title: str) -> str:
        """Extract law name from filename or title."""
        # Try to extract from filename first
        filename = os.path.basename(file_path)
        name_without_ext = os.path.splitext(filename)[0]
        
        # Clean up the name
        name_without_ext = re.sub(r'[_-]', ' ', name_without_ext)
        
        # If filename is too generic, try to use title
        if len(name_without_ext.split()) <= 2 and title and len(title) > 5:
            return title
            
        return name_without_ext
    
    def _process_pdf(self, file_path: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
        """
        Process a single PDF file and convert it to Document objects.
        
        Args:
            file_path: Path to the PDF file
            chunk_size: Size of text chunks in characters
            chunk_overlap: Overlap between chunks in characters
            
        Returns:
            List of Document objects
        """
        documents = []
        try:
            pdf_document = fitz.open(file_path)
            metadata = self._extract_metadata(pdf_document, file_path)
            
            # Extract text from each page
            full_text = ""
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                text = page.get_text()
                if text.strip():  # Only add non-empty pages
                    full_text += text + "\n\n"
            
            # Analyze document structure
            try:
                structure = self.structure_analyzer.analyze_document_structure(full_text)
            except Exception as e:
                print(f"Error analyzing document structure: {e}")
                structure = {"articles": [], "sections": []}
            
            # Store structure information in metadata (as flat values to avoid ChromaDB errors)
            metadata["article_count"] = len(structure.get("articles", []))
            metadata["section_count"] = len(structure.get("sections", []))
            
            # Create chunks with overlap
            if full_text:
                # First, create document-level chunk for full-text search
                full_doc_metadata = metadata.copy()
                full_doc_metadata["chunk_type"] = "full_document"
                documents.append(
                    Document(
                        page_content=full_text[:50000],  # Limit to avoid token limits
                        metadata=full_doc_metadata
                    )
                )
                
                # Then create regular chunks for retrieval
                chunks = []
                for i in range(0, len(full_text), chunk_size - chunk_overlap):
                    chunk = full_text[i:i + chunk_size]
                    if len(chunk) < 100:  # Skip very small chunks
                        continue
                    
                    chunk_metadata = metadata.copy()
                    chunk_metadata["chunk_id"] = len(chunks)
                    chunk_metadata["chunk_type"] = "text_chunk"
                    
                    # Check if this chunk contains any articles or sections
                    chunk_articles = self.structure_analyzer.extract_articles(chunk)
                    chunk_sections = self.structure_analyzer.extract_sections(chunk)
                    
                    if chunk_articles:
                        chunk_metadata["contains_articles"] = [art["id"] for art in chunk_articles]
                    if chunk_sections:
                        chunk_metadata["contains_sections"] = [sec["id"] for sec in chunk_sections]
                    
                    documents.append(
                        Document(
                            page_content=chunk,
                            metadata=chunk_metadata
                        )
                    )
                    chunks.append(chunk)
                
                # Create article-specific chunks
                if "articles" in structure and structure["articles"]:
                    for article in structure["articles"]:
                        article_metadata = metadata.copy()
                        article_metadata["chunk_type"] = "article"
                        article_metadata["article_id"] = article["id"]
                        # Avoid storing the full content in metadata
                        article_metadata["article_title"] = article.get("title", "")
                        
                        documents.append(
                            Document(
                                page_content=article["content"],
                                metadata=article_metadata
                            )
                        )
                
                # Create section-specific chunks
                if "sections" in structure and structure["sections"]:
                    for section in structure["sections"]:
                        section_metadata = metadata.copy()
                        section_metadata["chunk_type"] = "section"
                        section_metadata["section_id"] = section["id"]
                        # Avoid storing the full content in metadata
                        section_metadata["section_title"] = section.get("title", "")
                        
                        documents.append(
                            Document(
                                page_content=section["content"],
                                metadata=section_metadata
                            )
                        )
            
            pdf_document.close()
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
        
        return documents
    
    def load_documents(self, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
        """
        Load all PDF documents from the directory.
        
        Args:
            chunk_size: Size of text chunks in characters
            chunk_overlap: Overlap between chunks in characters
            
        Returns:
            List of Document objects
        """
        all_documents = []
        
        if not os.path.exists(self.directory_path):
            print(f"Directory {self.directory_path} does not exist.")
            return all_documents
        
        pdf_files = [
            os.path.join(self.directory_path, f) 
            for f in os.listdir(self.directory_path) 
            if f.lower().endswith('.pdf')
        ]
        
        if not pdf_files:
            print(f"No PDF files found in {self.directory_path}")
            return all_documents
        
        print(f"Processing {len(pdf_files)} PDF files...")
        for pdf_file in tqdm(pdf_files):
            documents = self._process_pdf(pdf_file, chunk_size, chunk_overlap)
            all_documents.extend(documents)
            
        print(f"Processed {len(all_documents)} document chunks from {len(pdf_files)} files.")
        return all_documents
    
    def find_article(self, documents: List[Document], article_number: str, law_name: Optional[str] = None) -> Optional[Document]:
        """
        Find a specific article in the loaded documents.
        
        Args:
            documents: List of Document objects
            article_number: Article number to find
            law_name: Optional law name to narrow down the search
            
        Returns:
            Document containing the article or None if not found
        """
        # First, try to find exact article chunks
        for doc in documents:
            if doc.metadata.get("chunk_type") == "article" and doc.metadata.get("article_id") == article_number:
                # If law name is specified, check if it matches
                if law_name:
                    doc_law_name = doc.metadata.get("law_name", "")
                    if law_name.lower() not in doc_law_name.lower():
                        continue
                return doc
        
        # If not found, try to find chunks containing the article
        for doc in documents:
            if doc.metadata.get("contains_articles") and article_number in doc.metadata.get("contains_articles", []):
                # If law name is specified, check if it matches
                if law_name:
                    doc_law_name = doc.metadata.get("law_name", "")
                    if law_name.lower() not in doc_law_name.lower():
                        continue
                    
                # Extract the article from the chunk
                article = self.structure_analyzer.find_article_by_number(doc.page_content, article_number)
                if article:
                    # Create a new document with just the article content
                    article_metadata = doc.metadata.copy()
                    article_metadata["chunk_type"] = "article"
                    article_metadata["article_id"] = article_number
                    
                    return Document(
                        page_content=article["content"],
                        metadata=article_metadata
                    )
        
        return None
    
    def find_section(self, documents: List[Document], section_number: str, law_name: Optional[str] = None) -> Optional[Document]:
        """
        Find a specific section in the loaded documents.
        
        Args:
            documents: List of Document objects
            section_number: Section number to find
            law_name: Optional law name to narrow down the search
            
        Returns:
            Document containing the section or None if not found
        """
        # First, try to find exact section chunks
        for doc in documents:
            if doc.metadata.get("chunk_type") == "section" and doc.metadata.get("section_id") == section_number:
                # If law name is specified, check if it matches
                if law_name:
                    doc_law_name = doc.metadata.get("law_name", "")
                    if law_name.lower() not in doc_law_name.lower():
                        continue
                return doc
        
        # If not found, try to find chunks containing the section
        for doc in documents:
            if doc.metadata.get("contains_sections") and section_number in doc.metadata.get("contains_sections", []):
                # If law name is specified, check if it matches
                if law_name:
                    doc_law_name = doc.metadata.get("law_name", "")
                    if law_name.lower() not in doc_law_name.lower():
                        continue
                    
                # Extract the section from the chunk
                section = self.structure_analyzer.find_section_by_number(doc.page_content, section_number)
                if section:
                    # Create a new document with just the section content
                    section_metadata = doc.metadata.copy()
                    section_metadata["chunk_type"] = "section"
                    section_metadata["section_id"] = section_number
                    
                    return Document(
                        page_content=section["content"],
                        metadata=section_metadata
                    )
        
        return None


if __name__ == "__main__":
    # Example usage
    loader = LegalDocumentLoader("src/data")
    documents = loader.load_documents()
    print(f"Loaded {len(documents)} document chunks.")
