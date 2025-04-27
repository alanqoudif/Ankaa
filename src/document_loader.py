"""
Document loader for parsing PDF files of Omani legal documents.
Supports both Arabic and English documents.
"""

import os
import fitz  # PyMuPDF
from typing import List, Dict, Optional
from langchain.schema import Document
from tqdm import tqdm

class LegalDocumentLoader:
    """Loader for Omani legal documents in PDF format."""
    
    def __init__(self, directory_path: str):
        """
        Initialize the document loader.
        
        Args:
            directory_path: Path to the directory containing PDF documents
        """
        self.directory_path = directory_path
        
    def _extract_metadata(self, pdf_document) -> Dict:
        """Extract metadata from PDF document."""
        metadata = pdf_document.metadata
        if metadata:
            return {
                "title": metadata.get("title", ""),
                "author": metadata.get("author", ""),
                "subject": metadata.get("subject", ""),
                "creator": metadata.get("creator", ""),
                "producer": metadata.get("producer", ""),
                "creation_date": metadata.get("creationDate", ""),
                "modification_date": metadata.get("modDate", ""),
                "page_count": pdf_document.page_count
            }
        return {"page_count": pdf_document.page_count}
    
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
            metadata = self._extract_metadata(pdf_document)
            metadata["source"] = file_path
            
            # Extract text from each page
            full_text = ""
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                text = page.get_text()
                if text.strip():  # Only add non-empty pages
                    full_text += text + "\n\n"
            
            # Create chunks with overlap
            if full_text:
                chunks = []
                for i in range(0, len(full_text), chunk_size - chunk_overlap):
                    chunk = full_text[i:i + chunk_size]
                    if len(chunk) < 100:  # Skip very small chunks
                        continue
                    
                    chunk_metadata = metadata.copy()
                    chunk_metadata["chunk_id"] = len(chunks)
                    
                    documents.append(
                        Document(
                            page_content=chunk,
                            metadata=chunk_metadata
                        )
                    )
                    chunks.append(chunk)
            
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


if __name__ == "__main__":
    # Example usage
    loader = LegalDocumentLoader("src/data")
    documents = loader.load_documents()
    print(f"Loaded {len(documents)} document chunks.")
