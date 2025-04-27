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
import numpy as np
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Use updated imports to avoid deprecation warnings
try:
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.embeddings import FastEmbedEmbeddings
except ImportError:
    # Fallback to old imports if new ones are not available
    from langchain.vectorstores import Chroma
    from langchain.embeddings import HuggingFaceEmbeddings

class DocumentEmbedder:
    """Generates and stores embeddings for legal document chunks."""
    
    def __init__(self, persist_directory: str = "chroma_db"):
        """
        Initialize the DocumentEmbedder.
        
        Args:
            persist_directory: Directory to persist the vector store
        """
        self.persist_directory = persist_directory
        os.makedirs(persist_directory, exist_ok=True)
        
        # Initialize embeddings model - use a lighter model to avoid memory issues
        try:
            # Try to use FastEmbedEmbeddings which is more memory efficient
            self.embeddings = FastEmbedEmbeddings()
        except (ImportError, Exception):
            # Fallback to HuggingFaceEmbeddings with minimal settings
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'}
            )
        
        # Try to load existing vector store if it exists
        if os.path.exists(os.path.join(persist_directory, "chroma.sqlite3")):
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
        # Force garbage collection to free memory
        gc.collect()
        
        # Create vector store
        self.vector_store = Chroma(
            collection_name="legal_documents",
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory
        )
        
        # Process documents in very small batches to avoid memory issues
        print(f"Creating embeddings for {len(documents)} documents...")
        batch_size = 100  # Smaller batch size to avoid memory issues
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
    
    def get_all_documents(self) -> List[Document]:
        """
        Get all documents stored in the vector store.
        
        Returns:
            List of all Document objects in the vector store
        """
        if self.vector_store is None:
            raise ValueError("Vector store not initialized. Please create embeddings first.")
        
        # Get all document IDs from the collection
        collection = self.vector_store._collection
        ids = collection.get()['ids']
        
        # Retrieve all documents
        all_docs = []
        for doc_id in ids:
            # Get the document by ID
            result = collection.get(ids=[doc_id])
            if result and result['documents'] and result['metadatas']:
                # Create Document object
                doc = Document(
                    page_content=result['documents'][0],
                    metadata=result['metadatas'][0]
                )
                all_docs.append(doc)
        
        return all_docs


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
