"""
Main application for the Sultanate Legal AI Assistant.
Provides a Streamlit interface for interacting with the legal QA system.
"""

import os
import streamlit as st
from document_loader import LegalDocumentLoader
from embeddings import DocumentEmbedder
from retriever import LegalDocumentRetriever
from llm_chain import LegalQAChain
from ui.components import (
    render_header, 
    render_chat_message, 
    render_info_box, 
    render_system_status,
    render_welcome_message,
    render_source_documents
)
from utils.model_utils import check_model_availability, get_recommended_models
from utils.ollama_utils import list_ollama_models, is_ollama_running

# Set page configuration
st.set_page_config(
    page_title="Sultanate Legal AI Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
DATA_DIR = "src/data"
CHROMA_DIR = "chroma_db"
MODEL_DIR = "models"
DEFAULT_MODEL_PATH = os.path.join(MODEL_DIR, "llama-2-7b-chat.ggmlv3.q4_0.bin")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "initialized" not in st.session_state:
    st.session_state.initialized = False
if "documents_loaded" not in st.session_state:
    st.session_state.documents_loaded = 0
if "embeddings_created" not in st.session_state:
    st.session_state.embeddings_created = False
if "model_loaded" not in st.session_state:
    st.session_state.model_loaded = False
if "model_name" not in st.session_state:
    st.session_state.model_name = "None"
if "show_sources" not in st.session_state:
    st.session_state.show_sources = False
if "current_sources" not in st.session_state:
    st.session_state.current_sources = []

# Render header
render_header()

# Sidebar
with st.sidebar:
    st.markdown("## System Configuration")
    
    # Model selection
    st.markdown("### LLM Model")
    
    # Model source selection
    model_source = st.radio(
        "Model Source",
        options=["Local Model", "Ollama"],
        horizontal=True
    )
    
    use_ollama = model_source == "Ollama"
    
    if use_ollama:
        # Check if Ollama is running
        if is_ollama_running():
            # Get available Ollama models
            ollama_models = list_ollama_models()
            if ollama_models:
                ollama_model_names = [model.get("name") for model in ollama_models]
                selected_ollama_model = st.selectbox("Select Ollama Model", ollama_model_names)
                model_path = "" # Not used with Ollama
            else:
                st.warning("No Ollama models found. Please pull some models using 'ollama pull <model_name>'")
                selected_ollama_model = "llama2"
                model_path = ""
        else:
            st.error("Ollama is not running. Please start Ollama and refresh this page.")
            selected_ollama_model = "llama2"
            model_path = ""
    else:
        # Local model selection
        models = get_recommended_models()
        model_options = ["Custom Path"] + [model["name"] for model in models]
        selected_model = st.selectbox("Select Model", model_options)
        
        if selected_model == "Custom Path":
            model_path = st.text_input("Model Path", value=DEFAULT_MODEL_PATH)
        else:
            # Find the selected model in the list
            selected_model_info = next((model for model in models if model["name"] == selected_model), None)
            if selected_model_info:
                model_path = selected_model_info["path"]
                if not check_model_availability(model_path):
                    st.warning(f"Model not found at {model_path}. Please download it first.")
    
    # Document processing options
    st.markdown("### Document Processing")
    chunk_size = st.slider("Chunk Size", min_value=500, max_value=2000, value=1000, step=100)
    chunk_overlap = st.slider("Chunk Overlap", min_value=0, max_value=500, value=200, step=50)
    
    # Retrieval options
    st.markdown("### Retrieval Options")
    top_k = st.slider("Number of Documents to Retrieve", min_value=1, max_value=10, value=4, step=1)
    
    # Initialize system
    init_col1, init_col2 = st.columns(2)
    with init_col1:
        if st.button("Load Documents"):
            with st.spinner("Loading documents..."):
                # Create directories if they don't exist
                os.makedirs(DATA_DIR, exist_ok=True)
                os.makedirs(MODEL_DIR, exist_ok=True)
                
                # Check if there are documents to load
                if not os.path.exists(DATA_DIR) or len([f for f in os.listdir(DATA_DIR) if f.lower().endswith('.pdf')]) == 0:
                    st.error("No PDF documents found in the data directory. Please add some PDF files to the src/data directory.")
                else:
                    # Load documents
                    loader = LegalDocumentLoader(DATA_DIR)
                    documents = loader.load_documents(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
                    
                    if documents:
                        st.session_state.documents = documents
                        st.session_state.documents_loaded = len(documents)
                        st.success(f"Successfully loaded {len(documents)} document chunks.")
                    else:
                        st.error("Failed to load documents. Please check the console for errors.")
    
    with init_col2:
        if st.button("Create Embeddings"):
            if not st.session_state.documents_loaded:
                st.error("Please load documents first.")
            else:
                with st.spinner("Creating embeddings..."):
                    # Create embeddings
                    embedder = DocumentEmbedder(persist_directory=CHROMA_DIR)
                    embedder.create_embeddings(st.session_state.documents)
                    
                    st.session_state.embedder = embedder
                    st.session_state.embeddings_created = True
                    st.success("Embeddings created successfully.")
    
    if st.button("Initialize System"):
        if not st.session_state.embeddings_created:
            st.error("Please load documents and create embeddings first.")
        elif not use_ollama and not os.path.exists(model_path):
            st.error(f"Model file not found at {model_path}. Please download the model or update the path.")
        elif use_ollama and not is_ollama_running():
            st.error("Ollama is not running. Please start Ollama and try again.")
        else:
            with st.spinner("Initializing system..."):
                # Initialize retriever and QA chain
                retriever = LegalDocumentRetriever(st.session_state.embedder, top_k=top_k)
                
                if use_ollama:
                    qa_chain = LegalQAChain(
                        use_ollama=True,
                        ollama_model=selected_ollama_model,
                        temperature=0.1,
                        max_tokens=2000
                    )
                    model_name = f"Ollama: {selected_ollama_model}"
                else:
                    qa_chain = LegalQAChain(model_path=model_path)
                    model_name = os.path.basename(model_path)
                
                st.session_state.retriever = retriever
                st.session_state.qa_chain = qa_chain
                st.session_state.initialized = True
                st.session_state.model_loaded = True
                st.session_state.model_name = model_name
                st.success("System initialized successfully.")
    
    # System status
    render_system_status({
        "documents_loaded": st.session_state.documents_loaded,
        "embeddings_created": st.session_state.embeddings_created,
        "model_loaded": st.session_state.model_loaded,
        "model_name": st.session_state.model_name,
        "system_initialized": st.session_state.initialized
    })
    
    # About section
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    **Sultanate Legal AI Assistant** is a smart chatbot that can answer questions about Omani laws based solely on the provided legal documents.
    
    This system does not use external knowledge and will only answer based on the documents it has been trained on.
    """)

# Main content area - Chat interface
st.markdown("## Chat Interface")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
    
    # Show sources after assistant messages if available
    if message["role"] == "assistant" and "sources" in message:
        with st.expander("View Sources", expanded=False):
            for i, source in enumerate(message["sources"]):
                st.markdown(f"**Source {i+1}:** {source['source']}")
                st.text_area(f"Content {i+1}", source["content"], height=150, key=f"source_{i}_{len(st.session_state.messages)}")

# Chat input
if prompt := st.chat_input("Ask a question about Omani laws..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    if not st.session_state.initialized:
        response = "The system has not been initialized yet. Please load documents, create embeddings, and initialize the system using the sidebar controls."
        sources = []
    else:
        with st.spinner("Searching for relevant information..."):
            # Retrieve relevant documents
            documents = st.session_state.retriever.retrieve(prompt)
            
            # Prepare context for the LLM
            context = st.session_state.retriever.get_relevant_text(prompt)
            
            # Generate answer
            response = st.session_state.qa_chain.answer_question(prompt, context)
            
            # Prepare sources for display
            sources = []
            for i, doc in enumerate(documents):
                source = doc.metadata.get("source", "Unknown source")
                # Extract just the filename from the path
                if "/" in source:
                    source = source.split("/")[-1]
                
                sources.append({
                    "source": source,
                    "content": doc.page_content
                })
    
    # Add assistant response to chat history with sources
    message = {
        "role": "assistant", 
        "content": response
    }
    if sources:
        message["sources"] = sources
    
    st.session_state.messages.append(message)
    
    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)
    
    # Show sources if available
    if sources:
        with st.expander("View Sources", expanded=False):
            for i, source in enumerate(sources):
                st.markdown(f"**Source {i+1}:** {source['source']}")
                st.text_area(f"Content {i+1}", source["content"], height=150, key=f"source_{i}_{len(st.session_state.messages)}")

# Instructions for first-time users
if not st.session_state.messages:
    render_welcome_message()


if __name__ == "__main__":
    # This will be executed when the script is run directly
    pass
