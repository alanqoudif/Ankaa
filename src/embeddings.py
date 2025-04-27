"""
Embeddings generator for legal documents.
Converts document chunks into vector embeddings for efficient retrieval.
"""

import os
from typing import List, Dict, Any
import os
import pickle
import gc
import time
import torch
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Use updated imports to avoid deprecation warnings
try:
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import HuggingFaceEmbeddings
except ImportError:
    # Fallback to old imports if new ones are not available
    from langchain.vectorstores import Chroma
    from langchain.embeddings import HuggingFaceEmbeddings

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
        Create embeddings for the documents and store them in the vector store.
        
        Args:
            documents: List of Document objects to create embeddings for
        """
        # Clear GPU memory if available
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        # Force garbage collection to free memory
        gc.collect()
        
        # Initialize embeddings model with optimized settings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        
        # Create vector store
        self.vector_store = Chroma(
            collection_name="legal_documents",
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory
        )
        
        # Process documents in smaller batches to avoid memory issues
        print(f"Creating embeddings for {len(documents)} documents...")
        batch_size = 500  # Adjust based on available memory
        total_batches = (len(documents) + batch_size - 1) // batch_size
        
        for i in range(0, len(documents), batch_size):
            batch_end = min(i + batch_size, len(documents))
            batch = documents[i:batch_end]
            print(f"Processing batch {(i // batch_size) + 1}/{total_batches} ({len(batch)} documents)")
            
            # Add documents to vector store
            self.vector_store.add_documents(batch)
            
            # Persist after each batch
            self.vector_store.persist()
            
            # Free memory
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
            # Small delay to allow system to stabilize
            time.sleep(1)
        
        print("Embedding creation completed successfully.")
        print(f"Embeddings created and stored in {self.persist_directory}")
    
    def add_documents(self, documents: List[Document]) -> None:
        """
        Add documents to an existing vector store.
        
        Args:
            documents: List of Document objects to add
        """
        if self.vector_store is None:
            raise ValueError("Vector store not initialized. Please create embeddings first.")
        
        # Add documents to vector store
        self.vector_store.add_documents(documents)
        self.vector_store.persist()
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """
        Perform similarity search for the query.
        
        Args:
            query: Query string
            k: Number of results to return
            
        Returns:
            List of Document objects most similar to the query
        """
        if self.vector_store is None:
            raise ValueError("Vector store not initialized. Please create embeddings first.")
            
        return self.vector_store.similarity_search(query, k=k)


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
