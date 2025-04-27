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
from ui.voice_components import (
    render_voice_input_button,
    render_text_to_speech_button,
    render_voice_status,
    download_vosk_model
)
from utils.model_utils import check_model_availability, get_recommended_models
from utils.ollama_utils import list_ollama_models, is_ollama_running
from utils.voice_utils import VoiceProcessor, TextToSpeech
from utils.comparison_utils import DocumentComparator

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
        "system_initialized": "System initialized successfully",
        "no_model_selected": "Please select a valid model!",
        "create_embeddings_first": "Please create embeddings first!",
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
        "no_ollama_models": "No Ollama models found. Please pull at least one model using 'ollama pull <model_name>'.",
        "article_not_found": "I couldn't find Article {article_number} in the legal documents. Please check the article number and try again.",
        "section_not_found": "I couldn't find Section {section_number} in the legal documents. Please check the section number and try again.",
        "summarizing": "Summarizing the content...",
        "summary_title": "Summary of {item_type} {item_number}",
        "from_law": "from {law_name}",
        "download_vosk_model": "Download Vosk Model for Offline Voice Recognition",
        "voice_input": "Voice Input",
        "processing_voice": "Processing your voice input...",
        "read_aloud": "Read Aloud",
        "comparison_results": "Comparison Results",
        "laws_compared": "Laws Compared",
        "comparison_topic": "Comparison Topic"
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
        "system_initialized": "تم تهيئة النظام بنجاح",
        "no_model_selected": "يرجى اختيار نموذج صالح!",
        "create_embeddings_first": "يرجى إنشاء التضمينات أولاً!",
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
        "no_ollama_models": "لم يتم العثور على نماذج أولاما. يرجى سحب نموذج واحد على الأقل باستخدام 'ollama pull <اسم_النموذج>'.",
        "article_not_found": "لم أتمكن من العثور على المادة {article_number} في المستندات القانونية. يرجى التحقق من رقم المادة والمحاولة مرة أخرى.",
        "section_not_found": "لم أتمكن من العثور على القسم {section_number} في المستندات القانونية. يرجى التحقق من رقم القسم والمحاولة مرة أخرى.",
        "summarizing": "جاري تلخيص المحتوى...",
        "summary_title": "ملخص {item_type} {item_number}",
        "from_law": "من {law_name}",
        "download_vosk_model": "تحميل نموذج Vosk للتعرف على الصوت بدون إنترنت",
        "voice_input": "إدخال صوتي",
        "processing_voice": "جاري معالجة المدخلات الصوتية...",
        "read_aloud": "قراءة بصوت عالٍ",
        "comparison_results": "نتائج المقارنة",
        "laws_compared": "القوانين التي تمت مقارنتها",
        "comparison_topic": "موضوع المقارنة"
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
if "embedder" not in st.session_state:
    st.session_state.embedder = None
if "retriever" not in st.session_state:
    st.session_state.retriever = None
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None
if "voice_processor" not in st.session_state:
    st.session_state.voice_processor = None
if "tts_engine" not in st.session_state:
    st.session_state.tts_engine = None
if "document_comparator" not in st.session_state:
    st.session_state.document_comparator = None
if "is_recording" not in st.session_state:
    st.session_state.is_recording = False

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
    
    # Initialize system buttons
    init_col1, init_col2, init_col3 = st.columns(3)
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
            if not st.session_state.get("documents_loaded", 0):
                st.error(t("create_embeddings_first"))
            else:
                with st.spinner(t("create_embeddings")):
                    try:
                        # Use a progress bar for better user feedback
                        progress_bar = st.progress(0)
                        
                        # Initialize embedder with optimized settings
                        embedder = DocumentEmbedder(persist_directory=CHROMA_DIR)
                        
                        # Get total document count for progress calculation
                        total_docs = len(st.session_state.documents)
                        batch_size = 500
                        total_batches = (total_docs + batch_size - 1) // batch_size
                        
                        # Process documents in smaller batches to avoid memory issues
                        for i in range(0, total_docs, batch_size):
                            batch_end = min(i + batch_size, total_docs)
                            batch = st.session_state.documents[i:batch_end]
                            
                            # Update status message
                            batch_num = (i // batch_size) + 1
                            st.markdown(f"Processing batch {batch_num}/{total_batches} ({len(batch)} documents)")
                            
                            # Update progress bar
                            progress = min(i / total_docs, 0.99) if total_docs > 0 else 0.99
                            progress_bar.progress(progress)
                            
                            # Process this batch if it's the first one, otherwise add to existing embeddings
                            if i == 0:
                                embedder.create_embeddings(batch)
                            else:
                                embedder.add_documents(batch)
                        
                        # Complete the progress bar
                        progress_bar.progress(1.0)
                        
                        # Store in session state
                        st.session_state.embedder = embedder
                        st.session_state.embeddings_created = True
                        st.success(t("embeddings_created"))
                    except Exception as e:
                        st.error(f"Error creating embeddings: {str(e)}")
                        import traceback
                        st.error(traceback.format_exc())
    
    # Add a third column for the Initialize System button
    with init_col3:
        if st.button(t("initialize_system")):
            if not st.session_state.get("embeddings_created", False):
                st.error(t("create_embeddings_first"))
            elif not model_path and not (use_ollama and selected_ollama_model):
                st.error(t("no_model_selected"))
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
                    
                    # Initialize voice processor and text-to-speech engine
                    st.session_state.voice_processor = VoiceProcessor()
                    st.session_state.tts_engine = TextToSpeech()
                    
                    # Initialize document comparator
                    st.session_state.document_comparator = DocumentComparator(st.session_state.embedder)
                    
                    st.success(t("system_initialized"))
    
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
            try:
                # Use a progress bar for better user feedback
                progress_bar = st.progress(0)
                
                # Initialize embedder with optimized settings
                embedder = DocumentEmbedder(persist_directory=CHROMA_DIR)
                
                # Get total document count for progress calculation
                total_docs = len(st.session_state.documents)
                batch_size = 500
                total_batches = (total_docs + batch_size - 1) // batch_size
                
                # Process documents in smaller batches to avoid memory issues
                for i in range(0, total_docs, batch_size):
                    batch_end = min(i + batch_size, total_docs)
                    batch = st.session_state.documents[i:batch_end]
                    
                    # Update status message
                    batch_num = (i // batch_size) + 1
                    st.markdown(f"Processing batch {batch_num}/{total_batches} ({len(batch)} documents)")
                    
                    # Update progress bar
                    progress = min(i / total_docs, 0.99) if total_docs > 0 else 0.99
                    progress_bar.progress(progress)
                    
                    # Process this batch if it's the first one, otherwise add to existing embeddings
                    if i == 0:
                        embedder.create_embeddings(batch)
                    else:
                        embedder.add_documents(batch)
                
                # Complete the progress bar
                progress_bar.progress(1.0)
                
                # Store in session state
                st.session_state.embedder = embedder
                st.session_state.embeddings_created = True
                # Make sure the embedder is properly initialized before continuing
                if st.session_state.embedder is None:
                    st.error("Failed to initialize embedder. Please try again.")
                    st.stop()
                st.success(t("embeddings_created"))
            except Exception as e:
                st.error(f"Error creating embeddings: {str(e)}")
                import traceback
                st.error(traceback.format_exc())
        
        # Step 3: Initialize system
        if not model_path and not (use_ollama and selected_ollama_model):
            st.error(t("no_model_selected"))
        else:
            with st.spinner(t("initialize_system")):
                # Check if embedder is initialized
                if st.session_state.embedder is None:
                    st.error("Embedder not initialized. Please create embeddings first.")
                    st.stop()
                    
                # Create retriever
                try:
                    retriever = LegalDocumentRetriever(st.session_state.embedder, top_k=top_k)
                    st.session_state.retriever = retriever
                except Exception as e:
                    st.error(f"Error creating retriever: {str(e)}")
                    st.stop()
                
                # Create QA chain
                if use_ollama:
                    from llm_chain import create_ollama_chain
                    qa_chain = create_ollama_chain(selected_ollama_model)
                else:
                    from llm_chain import create_local_chain
                    qa_chain = create_local_chain(model_path)
                
                st.session_state.qa_chain = qa_chain
                st.session_state.model_loaded = True
                st.session_state.model_name = selected_ollama_model if use_ollama else os.path.basename(model_path)
                
                # Initialize voice processor if dependencies are available
                try:
                    from utils.voice_utils import VoiceProcessor, TextToSpeech
                    
                    # Check for Vosk model
                    vosk_model_path = os.path.join(MODEL_DIR, "vosk-model-small-en-us-0.15")
                    use_vosk = os.path.exists(vosk_model_path) and os.path.isdir(vosk_model_path) and len(os.listdir(vosk_model_path)) > 0
                    
                    # Initialize voice processor
                    if use_vosk:
                        st.session_state.voice_processor = VoiceProcessor(use_vosk=True, model_path=vosk_model_path)
                        st.info(f"Voice processor initialized with Vosk model at {vosk_model_path}")
                    else:
                        # Use Whisper API if Vosk model is not available
                        st.session_state.voice_processor = VoiceProcessor(use_vosk=False)
                        st.info("Voice processor initialized with Whisper API (requires internet connection)")
                    
                    # Initialize text-to-speech engine
                    language = "ar" if st.session_state.language == "ar" else "en"
                    st.session_state.tts_engine = TextToSpeech(use_pyttsx3=True, language=language)
                    st.info("Text-to-speech engine initialized successfully")
                    
                except ImportError as e:
                    st.warning(f"Voice processing not available: {e}")
                    st.info("Install voice processing dependencies with: pip install vosk sounddevice soundfile pyttsx3 gtts")
                except Exception as e:
                    st.warning(f"Error initializing voice processing: {e}")
                
                # Initialize document comparator
                try:
                    from utils.comparison_utils import DocumentComparator
                    st.session_state.document_comparator = DocumentComparator(
                        retriever=st.session_state.retriever,
                        llm=qa_chain.llm,
                        language=st.session_state.language
                    )
                    st.info("Document comparison initialized successfully")
                except Exception as e:
                    st.warning(f"Error initializing document comparison: {e}")
                
                st.success(t("system_initialized"))
    
    # System status
    # Determine if a valid model is selected
    valid_model_selected = (model_path and os.path.exists(model_path)) or (use_ollama and selected_ollama_model)
    
    render_system_status({
        "documents_loaded": st.session_state.documents_loaded,
        "embeddings_created": st.session_state.embeddings_created,
        "model_loaded": valid_model_selected,
        "model_name": selected_ollama_model if use_ollama else (os.path.basename(model_path) if model_path else ""),
        "system_initialized": st.session_state.get("initialized", False)
    })
    
    # Add voice status to the sidebar
    # Check if voice processor is available
    voice_available = st.session_state.get("voice_processor") is not None
    
    # Create models directory if it doesn't exist
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    # Check if Vosk model exists
    vosk_model_path = os.path.join(MODEL_DIR, "vosk-model-small-en-us-0.15")
    vosk_model_exists = os.path.exists(vosk_model_path)
    
    # Display voice recognition status
    render_voice_status(is_available=voice_available, model_path=vosk_model_path if vosk_model_exists else None)
    
    # Add Vosk model download button if not already downloaded
    if not vosk_model_exists:
        download_vosk_model()
    
    # About section
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    **Sultanate Legal AI Assistant** is a smart chatbot that can answer questions about Omani laws based solely on the provided legal documents.
    
    This system does not use external knowledge and will only answer based on the documents it has been trained on.
    """)

# Function to format comparison results
def format_comparison_results(comparison_results):
    """Format the results of a cross-document comparison into a readable response."""
    response = f"## {t('comparison_results')}\n\n"
    
    # Add comparison topic if available
    if comparison_results.get("comparison_topic"):
        response += f"**{t('comparison_topic')}:** {comparison_results['comparison_topic']}\n\n"
    
    # Add laws compared
    response += f"**{t('laws_compared')}:** {', '.join(comparison_results['laws_compared'])}\n\n"
    
    # Add results for each law
    for law_name, law_data in comparison_results["results"].items():
        response += f"### {law_name}\n\n"
        
        # Add key points from this law
        if law_data.get("summary"):
            for i, point in enumerate(law_data["summary"], 1):
                response += f"{i}. {point}\n"
        
        response += "\n"
    
    return response

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

# Add voice input button and download model button if system is initialized
if st.session_state.initialized:
    # Add a section for voice tools
    st.markdown("### Voice Tools")
    
    # Check if Vosk model exists
    vosk_model_path = os.path.join(MODEL_DIR, "vosk-model-small-en-us-0.15")
    if not os.path.exists(vosk_model_path):
        # Show download button for Vosk model
        download_vosk_model()
    
    # Voice input callback function
    def on_voice_input(text):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": text})
        st.rerun()
    
    # Show voice input button if voice processor is available
    if st.session_state.voice_processor:
        render_voice_input_button(on_voice_input)
    else:
        st.warning(t("Voice input is not available. Please install the required dependencies."))

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
        # Check if this is a comparison query
        if ("compare" in prompt.lower() or "قارن" in prompt or "مقارنة" in prompt) and st.session_state.document_comparator:
            with st.spinner(t("processing")):
                comparison_results = st.session_state.document_comparator.compare_laws(prompt)
                
                if comparison_results["success"]:
                    # Format comparison results
                    response = format_comparison_results(comparison_results)
                    sources = []
                    for law_name, law_data in comparison_results["results"].items():
                        if law_data.get("documents"):
                            for doc in law_data["documents"]:
                                sources.append({
                                    "source": f"{law_name} - {doc.metadata.get('source', '')}",
                                    "content": doc.page_content
                                })
                else:
                    response = comparison_results["message"]
                    sources = []
        # Check if this is a request for a specific article or section
        else:
            doc, item_type, found = st.session_state.retriever.get_article_or_section(prompt)
            
            # If it's a request for a specific article or section
            if item_type in ["article", "section"]:
                if found:
                    # Get the item number and law name
                    item_number = doc.metadata.get(f"{item_type}_id", "")
                    law_name = doc.metadata.get("law_name", doc.metadata.get("filename", ""))
                    
                    # Check if this is a summarization request
                    is_summary_request = "summarize" in prompt.lower() or "تلخيص" in prompt or "لخص" in prompt
                    
                    if is_summary_request:
                        with st.spinner(t("summarizing")):
                            # Generate summary
                            summary = st.session_state.qa_chain.summarize_text(doc.page_content)
                            
                            # Format the response
                            item_type_display = "Article" if item_type == "article" else "Section"
                            if st.session_state.language == "ar":
                                item_type_display = "المادة" if item_type == "article" else "القسم"
                            
                            title = t("summary_title").format(item_type=item_type_display, item_number=item_number)
                            if law_name:
                                title += " " + t("from_law").format(law_name=law_name)
                            
                            response = f"**{title}**\n\n{summary}"
                    else:
                        # Just return the content of the article/section
                        item_type_display = "Article" if item_type == "article" else "Section"
                        if st.session_state.language == "ar":
                            item_type_display = "المادة" if item_type == "article" else "القسم"
                        
                        title = f"**{item_type_display} {item_number}**"
                        if law_name:
                            title += " " + t("from_law").format(law_name=law_name)
                        
                        response = f"{title}\n\n{doc.page_content}"
                    
                    # Add source information
                    sources = [{
                        "source": doc.metadata.get("filename", doc.metadata.get("source", "Unknown")),
                        "content": doc.page_content,
                        "metadata": doc.metadata
                    }]
                else:
                    # Article or section not found
                    if item_type == "article":
                        # Extract article number from query
                        import re
                        article_match = re.search(r'article\s+(\d+)|المادة\s+(\d+)|مادة\s+(\d+)', prompt.lower())
                        article_number = article_match.group(1) if article_match and article_match.group(1) else \
                                        article_match.group(2) if article_match and article_match.group(2) else \
                                        article_match.group(3) if article_match and article_match.group(3) else "?"
                        
                        response = t("article_not_found").format(article_number=article_number)
                    else:  # section
                        # Extract section number from query
                        import re
                        section_match = re.search(r'section\s+(\d+)|chapter\s+(\d+)|القسم\s+(\d+)|الفصل\s+(\d+)|الباب\s+(\d+)', prompt.lower())
                        section_number = section_match.group(1) if section_match and section_match.group(1) else \
                                        section_match.group(2) if section_match and section_match.group(2) else \
                                        section_match.group(3) if section_match and section_match.group(3) else \
                                        section_match.group(4) if section_match and section_match.group(4) else \
                                        section_match.group(5) if section_match and section_match.group(5) else "?"
                        
                        response = t("section_not_found").format(section_number=section_number)
                    
                    sources = []
            else:
                # Regular question answering
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
                        
                        # Create source object
                        sources.append({
                            "source": source,
                            "content": doc.page_content,
                            "metadata": doc.metadata
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
        
        # Add text-to-speech button for the response
        if st.session_state.tts_engine:
            render_text_to_speech_button(response)
    
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
