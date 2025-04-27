"""
Retriever module for the Legal AI Assistant.
Handles vector search and document retrieval based on user queries.
"""

from typing import List, Dict, Any
from langchain.schema import Document
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from embeddings import DocumentEmbedder

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
    
    def retrieve(self, query: str, k: int = None) -> List[Document]:
        """
        Retrieve relevant documents based on the query.
        
        Args:
            query: User query
            k: Number of documents to retrieve (overrides self.top_k if provided)
            
        Returns:
            List of relevant Document objects
        """
        # Use provided k or default to self.top_k
        top_k = k if k is not None else self.top_k
        
        # Perform similarity search
        documents = self.embedder.similarity_search(query, k=top_k)
        return documents
    
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
            
            result.append(f"Document {i+1} (Source: {source}):\n{doc.page_content}\n")
        
        return "\n".join(result)


if __name__ == "__main__":
    # Example usage
    embedder = DocumentEmbedder(persist_directory="chroma_db")
    retriever = LegalDocumentRetriever(embedder)
    
    # Test retrieval
    query = "What is the punishment for theft?"
    relevant_text = retriever.get_relevant_text(query)
    print(f"Query: {query}")
    print(f"Relevant text:\n{relevant_text}")
