"""
Embeddings generator for legal documents.
Converts document chunks into vector embeddings for efficient retrieval.
"""

import os
from typing import List, Dict, Any
from langchain.schema import Document
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.embeddings.base import Embeddings

class DocumentEmbedder:
    """Generates and stores embeddings for legal document chunks."""
    
    def __init__(
        self, 
        persist_directory: str = "chroma_db",
        embedding_model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    ):
        """
        Initialize the document embedder.
        
        Args:
            persist_directory: Directory to persist the vector database
            embedding_model_name: Name of the embedding model to use
        """
        self.persist_directory = persist_directory
        self.embedding_model_name = embedding_model_name
        
        # Create embeddings model - using a multilingual model to support both Arabic and English
        self.embeddings = HuggingFaceEmbeddings(
            model_name=embedding_model_name,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True}
        )
        
        # Initialize vector store if it exists
        if os.path.exists(persist_directory):
            self.vector_store = Chroma(
                persist_directory=persist_directory,
                embedding_function=self.embeddings
            )
        else:
            self.vector_store = None
    
    def create_embeddings(self, documents: List[Document]) -> None:
        """
        Create embeddings for documents and store them in the vector database.
        
        Args:
            documents: List of Document objects to embed
        """
        if not documents:
            print("No documents provided for embedding.")
            return
        
        print(f"Creating embeddings for {len(documents)} documents...")
        
        # Create new vector store or add to existing one
        if self.vector_store is None:
            self.vector_store = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=self.persist_directory
            )
        else:
            # Add documents to existing vector store
            self.vector_store.add_documents(documents)
        
        # Persist the vector store
        self.vector_store.persist()
        print(f"Embeddings created and stored in {self.persist_directory}")
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """
        Perform similarity search on the vector store.
        
        Args:
            query: Query string
            k: Number of results to return
            
        Returns:
            List of Document objects most similar to the query
        """
        if self.vector_store is None:
            print("Vector store not initialized. Please create embeddings first.")
            return []
        
        results = self.vector_store.similarity_search(query, k=k)
        return results


if __name__ == "__main__":
    # Example usage
    from document_loader import LegalDocumentLoader
    
    # Load documents
    loader = LegalDocumentLoader("src/data")
    documents = loader.load_documents()
    
    # Create embeddings
    embedder = DocumentEmbedder(persist_directory="chroma_db")
    embedder.create_embeddings(documents)
    
    # Test similarity search
    results = embedder.similarity_search("What is the punishment for theft?")
    for i, doc in enumerate(results):
        print(f"Result {i+1}:")
        print(f"Content: {doc.page_content[:200]}...")
        print(f"Source: {doc.metadata.get('source', 'Unknown')}")
        print("-" * 50)
