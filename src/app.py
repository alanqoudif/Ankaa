"""
Main application for the Sultanate Legal AI Assistant.
Provides a Streamlit interface for interacting with the legal QA system.
"""

import os
import time
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

# Dictionary for translations
TRANSLATIONS = {
    "en": {
        "app_title": "Sultanate Legal AI Assistant",
        "app_description": "An AI assistant for answering questions about Omani laws",
        "sidebar_title": "Settings",
        "language": "Language",
        "model_source": "Model Source",
        "local_model": "Local Model",
        "ollama": "Ollama",
        "model_selection": "Model Selection",
        "top_k": "Number of sources to retrieve",
        "system_status": "System Status",
        "load_documents": "Load Documents",
        "create_embeddings": "Create Embeddings",
        "initialize_system": "Initialize System",
        "setup_all": "Setup All (Load, Embed & Initialize)",
        "documents_loaded": "Documents loaded",
        "embeddings_created": "Embeddings created",
        "system_initialized": "System initialized",
        "chat_interface": "Chat Interface",
        "ask_placeholder": "Ask a question about Omani laws...",
        "processing": "Processing your question...",
        "searching": "Searching for relevant information...",
        "view_sources": "View Sources",
        "source": "Source",
        "content": "Content",
        "welcome_title": "Welcome to the Sultanate Legal AI Assistant!",
        "welcome_message": "I'm here to help answer your questions about Omani laws. To get started:",
        "welcome_step1": "1. Load the legal documents using the 'Load Documents' button",
        "welcome_step2": "2. Create embeddings using the 'Create Embeddings' button",
        "welcome_step3": "3. Initialize the system using the 'Initialize System' button",
        "welcome_step4": "4. Or simply click 'Setup All' to do all three steps at once",
        "welcome_step5": "5. Ask your questions in the chat box below",
        "ollama_not_running": "Ollama is not running. Please start Ollama to use Ollama models.",
        "no_ollama_models": "No Ollama models found. Please pull at least one model using 'ollama pull <model_name>'."
    },
    "ar": {
        "app_title": "المساعد القانوني الذكي لسلطنة عمان",
        "app_description": "مساعد ذكاء اصطناعي للإجابة على الأسئلة حول القوانين العمانية",
        "sidebar_title": "الإعدادات",
        "language": "اللغة",
        "model_source": "مصدر النموذج",
        "local_model": "نموذج محلي",
        "ollama": "أولاما",
        "model_selection": "اختيار النموذج",
        "top_k": "عدد المصادر المراد استرجاعها",
        "system_status": "حالة النظام",
        "load_documents": "تحميل المستندات",
        "create_embeddings": "إنشاء التضمينات",
        "initialize_system": "تهيئة النظام",
        "setup_all": "إعداد الكل (تحميل، تضمين وتهيئة)",
        "documents_loaded": "تم تحميل المستندات",
        "embeddings_created": "تم إنشاء التضمينات",
        "system_initialized": "تم تهيئة النظام",
        "chat_interface": "واجهة المحادثة",
        "ask_placeholder": "اسأل سؤالاً حول القوانين العمانية...",
        "processing": "جاري معالجة سؤالك...",
        "searching": "جاري البحث عن المعلومات ذات الصلة...",
        "view_sources": "عرض المصادر",
        "source": "المصدر",
        "content": "المحتوى",
        "welcome_title": "مرحبًا بك في المساعد القانوني الذكي لسلطنة عمان!",
        "welcome_message": "أنا هنا للمساعدة في الإجابة على أسئلتك حول القوانين العمانية. للبدء:",
        "welcome_step1": "1. قم بتحميل المستندات القانونية باستخدام زر 'تحميل المستندات'",
        "welcome_step2": "2. قم بإنشاء التضمينات باستخدام زر 'إنشاء التضمينات'",
        "welcome_step3": "3. قم بتهيئة النظام باستخدام زر 'تهيئة النظام'",
        "welcome_step4": "4. أو ببساطة انقر على 'إعداد الكل' للقيام بالخطوات الثلاث دفعة واحدة",
        "welcome_step5": "5. اطرح أسئلتك في مربع الدردشة أدناه",
        "ollama_not_running": "أولاما غير مشغل. يرجى تشغيل أولاما لاستخدام نماذج أولاما.",
        "no_ollama_models": "لم يتم العثور على نماذج أولاما. يرجى سحب نموذج واحد على الأقل باستخدام 'ollama pull <اسم_النموذج>'."
    }
}

# Initialize session state for language if not exists
if 'language' not in st.session_state:
    st.session_state.language = "en"

# Function to get translated text
def t(key):
    return TRANSLATIONS[st.session_state.language][key]

# Set page config
st.set_page_config(
    page_title=t("app_title"),
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
    
    # Language selection
    selected_language = st.selectbox(
        t("language"),
        options=["English", "العربية"],
        index=0 if st.session_state.language == "en" else 1
    )

    # Update language in session state
    if selected_language == "English" and st.session_state.language != "en":
        st.session_state.language = "en"
        st.rerun()
    elif selected_language == "العربية" and st.session_state.language != "ar":
        st.session_state.language = "ar"
        st.rerun()

    # Model selection
    st.markdown("### LLM Model")
    
    # Model source selection
    model_source = st.radio(
        t("model_source"),
        options=[t("local_model"), t("ollama")],
        horizontal=True
    )
    
    use_ollama = model_source == t("ollama")
    
    if use_ollama:
        # Check if Ollama is running
        if is_ollama_running():
            # Get available Ollama models
            ollama_models = list_ollama_models()
            if ollama_models:
                ollama_model_names = [model.get("name") for model in ollama_models]
                selected_ollama_model = st.selectbox(t("model_selection"), ollama_model_names)
                model_path = "" # Not used with Ollama
            else:
                st.warning(t("no_ollama_models"))
                selected_ollama_model = "llama2"
                model_path = ""
        else:
            st.error(t("ollama_not_running"))
            selected_ollama_model = "llama2"
            model_path = ""
    else:
        # Local model selection
        models = get_recommended_models()
        model_options = ["Custom Path"] + [model["name"] for model in models]
        selected_model = st.selectbox(t("model_selection"), model_options)
        
        if selected_model == "Custom Path":
            model_path = st.text_input(t("model_selection"), value=DEFAULT_MODEL_PATH)
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
    top_k = st.slider(t("top_k"), min_value=1, max_value=10, value=4, step=1)
    
    # Initialize system
    init_col1, init_col2 = st.columns(2)
    with init_col1:
        if st.button(t("load_documents")):
            with st.spinner(t("load_documents")):
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
        if st.button(t("create_embeddings")):
            if not st.session_state.documents_loaded:
                st.error("Please load documents first.")
            else:
                with st.spinner(t("create_embeddings")):
                    # Create embeddings
                    embedder = DocumentEmbedder(persist_directory=CHROMA_DIR)
                    embedder.create_embeddings(st.session_state.documents)
                    
                    st.session_state.embedder = embedder
                    st.session_state.embeddings_created = True
                    st.success("Embeddings created successfully.")
    
    # Setup All button (does all three steps)
    if st.button(t("setup_all"), type="primary", use_container_width=True):
        # Step 1: Load documents
        with st.spinner(t("load_documents")):
            document_loader = LegalDocumentLoader(DATA_DIR)
            documents = document_loader.load_documents(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            st.session_state.documents = documents
            st.session_state.documents_loaded = len(documents)
        
        # Step 2: Create embeddings
        with st.spinner(t("create_embeddings")):
            embedder = DocumentEmbedder(persist_directory=CHROMA_DIR)
            embedder.create_embeddings(st.session_state.documents)
            st.session_state.embedder = embedder
            st.session_state.embeddings_created = True
        
        # Step 3: Initialize system
        if not model_path:
            st.error("Please select a valid model!")
        else:
            with st.spinner(t("initialize_system")):
                # Create retriever
                retriever = LegalDocumentRetriever(st.session_state.embedder, top_k=top_k)
                st.session_state.retriever = retriever
                
                # Create QA chain
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
st.markdown(f"## {t('chat_interface')}")

# Display chat messages
for msg_idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
    
    # Show sources after assistant messages if available
    if message["role"] == "assistant" and "sources" in message:
        with st.expander(t("view_sources"), expanded=False):
            for i, source in enumerate(message["sources"]):
                st.markdown(f"**{t('source')} {i+1}:** {source['source']}")
                # Use unique key combining message index, source index and timestamp
                unique_key = f"source_{msg_idx}_{i}_{hash(message.get('timestamp', ''))}_{hash(source.get('source', ''))}"  
                st.text_area(f"{t('content')} {i+1}", source["content"], height=150, key=unique_key)

# Chat input
if prompt := st.chat_input(t("ask_placeholder")):
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
        with st.spinner(t("searching")):
            # Retrieve relevant documents with higher k to ensure we get enough relevant content
            documents = st.session_state.retriever.retrieve(prompt, k=top_k * 2)
            
            # Filter documents more precisely to find the most relevant ones for this specific query
            # This helps ensure we're reading files that are directly related to the user's question
            filtered_documents = []
            for doc in documents:
                # Simple relevance check - can be enhanced with more sophisticated methods
                if any(term.lower() in doc.page_content.lower() for term in prompt.lower().split()):
                    filtered_documents.append(doc)
            
            # Use at least top_k documents, even if filtering removed some
            if len(filtered_documents) < top_k and len(documents) >= top_k:
                filtered_documents = documents[:top_k]
            
            # Prepare context for the LLM using the filtered documents
            context = ""
            for doc in filtered_documents:
                source = doc.metadata.get("source", "Unknown source")
                if "/" in source:
                    source = source.split("/")[-1]
                context += f"\nSource: {source}\n{doc.page_content}\n\n"
            
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
        "content": response,
        "timestamp": str(int(time.time()))
    }
    if sources:
        message["sources"] = sources
    
    st.session_state.messages.append(message)
    
    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)
    
    # Show sources if available
    if sources:
        with st.expander(t("view_sources"), expanded=False):
            for i, source in enumerate(sources):
                st.markdown(f"**{t('source')} {i+1}:** {source['source']}")
                # Use unique key combining timestamp and source
                current_time = str(int(time.time()))
                unique_key = f"current_source_{i}_{hash(current_time)}_{hash(source.get('source', ''))}"  
                st.text_area(f"{t('content')} {i+1}", source["content"], height=150, key=unique_key)

# Instructions for first-time users
if not st.session_state.get("messages", []):
    render_welcome_message()


if __name__ == "__main__":
    # This will be executed when the script is run directly
    pass
