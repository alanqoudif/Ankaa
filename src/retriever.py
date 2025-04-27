"""
Retriever module for the Legal AI Assistant.
Handles vector search and document retrieval based on user queries.
"""

import re
from typing import List, Dict, Any, Optional, Tuple, Union
from langchain.schema import Document
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from embeddings import DocumentEmbedder
from document_loader import LegalDocumentLoader

class LegalDocumentRetriever:
    """Retriever for legal documents based on vector similarity search."""
    
    def __init__(
        self,
        embedder: DocumentEmbedder,
        top_k: int = 4,
    ):
        """
        Initialize the document retriever.
        
        Args:
            embedder: DocumentEmbedder instance
            top_k: Number of documents to retrieve
        """
        self.embedder = embedder
        self.top_k = top_k
        # Initialize document_loader lazily to avoid issues with Streamlit session state
        self._document_loader = None
        
    @property
    def document_loader(self):
        """Lazy initialization of document_loader"""
        if self._document_loader is None:
            self._document_loader = LegalDocumentLoader("src/data")
        return self._document_loader
    
    def retrieve(self, query: str, k: int = None) -> List[Document]:
        """
        Retrieve relevant documents based on the query.
        
        Args:
            query: User query
            k: Number of documents to retrieve (overrides self.top_k if provided)
            
        Returns:
            List of relevant Document objects
        """
        # Check if this is a request for a specific article or section
        article_match = self._check_for_article_request(query)
        if article_match:
            article_num, law_name = article_match
            return self._retrieve_article(article_num, law_name)
        
        section_match = self._check_for_section_request(query)
        if section_match:
            section_num, law_name = section_match
            return self._retrieve_section(section_num, law_name)
        
        # If not a specific article/section request, perform regular similarity search
        top_k = k if k is not None else self.top_k
        documents = self.embedder.similarity_search(query, k=top_k)
        return documents
    
    def _check_for_article_request(self, query: str) -> Optional[Tuple[str, Optional[str]]]:
        """
        Check if the query is requesting a specific article.
        
        Args:
            query: User query
            
        Returns:
            Tuple of (article_number, law_name) if found, None otherwise
        """
        # English patterns
        article_patterns = [
            r'article\s+(\d+)\s+(?:of|from)\s+(?:the\s+)?(.*?)(?:law|code|decree)',
            r'summarize\s+article\s+(\d+)\s+(?:of|from)\s+(?:the\s+)?(.*?)(?:law|code|decree)',
            # Arabic patterns
            r'المادة\s+(\d+)\s+من\s+(?:قانون|مرسوم)\s+(.*?)(?:\.|$)',
            r'قم\s+بتلخيص\s+المادة\s+(\d+)\s+من\s+(?:قانون|مرسوم)\s+(.*?)(?:\.|$)',
            # Simpler patterns
            r'article\s+(\d+)\s+(?:of|from)\s+(.*?)(?:\.|$)',
            r'المادة\s+(\d+)\s+من\s+(.*?)(?:\.|$)'
        ]
        
        for pattern in article_patterns:
            match = re.search(pattern, query.lower())
            if match:
                article_num = match.group(1)
                law_name = match.group(2).strip() if len(match.groups()) > 1 else None
                return article_num, law_name
        
        # Check for just article number without law name
        simple_patterns = [
            r'article\s+(\d+)',
            r'المادة\s+(\d+)',
            r'مادة\s+(\d+)'
        ]
        
        for pattern in simple_patterns:
            match = re.search(pattern, query.lower())
            if match:
                article_num = match.group(1)
                return article_num, None
        
        return None
    
    def _check_for_section_request(self, query: str) -> Optional[Tuple[str, Optional[str]]]:
        """
        Check if the query is requesting a specific section.
        
        Args:
            query: User query
            
        Returns:
            Tuple of (section_number, law_name) if found, None otherwise
        """
        # English patterns
        section_patterns = [
            r'section\s+(\d+)\s+(?:of|from)\s+(?:the\s+)?(.*?)(?:law|code|decree)',
            r'summarize\s+section\s+(\d+)\s+(?:of|from)\s+(?:the\s+)?(.*?)(?:law|code|decree)',
            r'chapter\s+(\d+)\s+(?:of|from)\s+(?:the\s+)?(.*?)(?:law|code|decree)',
            # Arabic patterns
            r'القسم\s+(\d+)\s+من\s+(?:قانون|مرسوم)\s+(.*?)(?:\.|$)',
            r'الفصل\s+(\d+)\s+من\s+(?:قانون|مرسوم)\s+(.*?)(?:\.|$)',
            r'الباب\s+(\d+)\s+من\s+(?:قانون|مرسوم)\s+(.*?)(?:\.|$)',
            # Simpler patterns
            r'section\s+(\d+)\s+(?:of|from)\s+(.*?)(?:\.|$)',
            r'chapter\s+(\d+)\s+(?:of|from)\s+(.*?)(?:\.|$)',
            r'القسم\s+(\d+)\s+من\s+(.*?)(?:\.|$)',
            r'الفصل\s+(\d+)\s+من\s+(.*?)(?:\.|$)',
            r'الباب\s+(\d+)\s+من\s+(.*?)(?:\.|$)'
        ]
        
        for pattern in section_patterns:
            match = re.search(pattern, query.lower())
            if match:
                section_num = match.group(1)
                law_name = match.group(2).strip() if len(match.groups()) > 1 else None
                return section_num, law_name
        
        # Check for just section number without law name
        simple_patterns = [
            r'section\s+(\d+)',
            r'chapter\s+(\d+)',
            r'القسم\s+(\d+)',
            r'الفصل\s+(\d+)',
            r'الباب\s+(\d+)'
        ]
        
        for pattern in simple_patterns:
            match = re.search(pattern, query.lower())
            if match:
                section_num = match.group(1)
                return section_num, None
        
        return None
    
    def _retrieve_article(self, article_number: str, law_name: Optional[str] = None) -> List[Document]:
        """
        Retrieve a specific article.
        
        Args:
            article_number: Article number to retrieve
            law_name: Optional law name to narrow down the search
            
        Returns:
            List containing the article document if found, empty list otherwise
        """
        # Get all documents from the embedder
        documents = self.embedder.get_all_documents()
        
        # Find the article
        article_doc = self.document_loader.find_article(documents, article_number, law_name)
        
        if article_doc:
            return [article_doc]
        return []
    
    def _retrieve_section(self, section_number: str, law_name: Optional[str] = None) -> List[Document]:
        """
        Retrieve a specific section.
        
        Args:
            section_number: Section number to retrieve
            law_name: Optional law name to narrow down the search
            
        Returns:
            List containing the section document if found, empty list otherwise
        """
        # Get all documents from the embedder
        documents = self.embedder.get_all_documents()
        
        # Find the section
        section_doc = self.document_loader.find_section(documents, section_number, law_name)
        
        if section_doc:
            return [section_doc]
        return []
    
    def get_relevant_text(self, query: str) -> str:
        """
        Get relevant text from retrieved documents as a single string.
        
        Args:
            query: User query
            
        Returns:
            String containing relevant text from retrieved documents
        """
        documents = self.retrieve(query)
        if not documents:
            return "No relevant information found."
        
        # Combine document contents with source information
        result = []
        for i, doc in enumerate(documents):
            source = doc.metadata.get("source", "Unknown source")
            # Extract just the filename from the path
            if "/" in source:
                source = source.split("/")[-1]
            
            # Check if this is an article or section
            chunk_type = doc.metadata.get("chunk_type", "")
            if chunk_type == "article":
                article_id = doc.metadata.get("article_id", "")
                result.append(f"Article {article_id} (Source: {source}):\n{doc.page_content}\n")
            elif chunk_type == "section":
                section_id = doc.metadata.get("section_id", "")
                result.append(f"Section {section_id} (Source: {source}):\n{doc.page_content}\n")
            else:
                result.append(f"Document {i+1} (Source: {source}):\n{doc.page_content}\n")
        
        return "\n".join(result)
    
    def get_article_or_section(self, query: str) -> Tuple[Optional[Document], str, bool]:
        """
        Check if the query is requesting a specific article or section and retrieve it.
        
        Args:
            query: User query
            
        Returns:
            Tuple of (document, type_name, found_flag)
            - document: The retrieved document or None if not found
            - type_name: "article" or "section"
            - found_flag: True if found, False otherwise
        """
        # Check for article request
        article_match = self._check_for_article_request(query)
        if article_match:
            article_num, law_name = article_match
            article_docs = self._retrieve_article(article_num, law_name)
            if article_docs:
                return article_docs[0], "article", True
            return None, "article", False
        
        # Check for section request
        section_match = self._check_for_section_request(query)
        if section_match:
            section_num, law_name = section_match
            section_docs = self._retrieve_section(section_num, law_name)
            if section_docs:
                return section_docs[0], "section", True
            return None, "section", False
        
        # Not a specific article or section request
        return None, "", False


if __name__ == "__main__":
    # Example usage
    embedder = DocumentEmbedder(persist_directory="chroma_db")
    retriever = LegalDocumentRetriever(embedder)
    
    # Test retrieval
    query = "What is the punishment for theft?"
    relevant_text = retriever.get_relevant_text(query)
    print(f"Query: {query}")
    print(f"Relevant text:\n{relevant_text}")
