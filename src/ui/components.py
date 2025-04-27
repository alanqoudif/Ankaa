"""
UI components for the Streamlit interface of the Legal AI Assistant.
"""

import streamlit as st
from typing import List, Dict, Any, Optional

def render_header():
    """Render the application header."""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #1E3A8A;">⚖️ Sultanate Legal AI Assistant</h1>
        <h3 style="color: #4B5563;">Smart Search Bot for Omani Legal Documents</h3>
    </div>
    """, unsafe_allow_html=True)

def render_chat_message(role: str, content: str, avatar: Optional[str] = None):
    """
    Render a chat message with styling.
    
    Args:
        role: Role of the message sender ('user' or 'assistant')
        content: Message content
        avatar: Optional avatar image path
    """
    if role == "user":
        st.markdown("""
        <div style="display: flex; margin-bottom: 15px;">
            <div style="background-color: #1E40AF; color: white; border-radius: 50%; width: 40px; height: 40px; 
                    display: flex; align-items: center; justify-content: center; margin-right: 10px; flex-shrink: 0;">
                <span>👤</span>
            </div>
            <div style="background-color: #E3F2FD; padding: 10px 15px; border-radius: 10px; max-width: 80%; border-left: 5px solid #1E88E5;">
                <p style="margin: 0;">{}</p>
            </div>
        </div>
        """.format(content), unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="display: flex; margin-bottom: 15px; justify-content: flex-end;">
            <div style="background-color: #F1F8E9; padding: 10px 15px; border-radius: 10px; max-width: 80%; border-left: 5px solid #43A047; text-align: left;">
                <p style="margin: 0;">{}</p>
            </div>
            <div style="background-color: #43A047; color: white; border-radius: 50%; width: 40px; height: 40px; 
                    display: flex; align-items: center; justify-content: center; margin-left: 10px; flex-shrink: 0;">
                <span>⚖️</span>
            </div>
        </div>
        """.format(content), unsafe_allow_html=True)

def render_info_box(title: str, content: str, box_type: str = "info"):
    """
    Render an information box with styling.
    
    Args:
        title: Box title
        content: Box content
        box_type: Box type ('info', 'success', 'warning', or 'error')
    """
    if box_type == "info":
        color = "#1E88E5"
        bg_color = "#E3F2FD"
        icon = "ℹ️"
    elif box_type == "success":
        color = "#43A047"
        bg_color = "#E8F5E9"
        icon = "✅"
    elif box_type == "warning":
        color = "#FB8C00"
        bg_color = "#FFF8E1"
        icon = "⚠️"
    elif box_type == "error":
        color = "#E53935"
        bg_color = "#FFEBEE"
        icon = "❌"
    else:
        color = "#1E88E5"
        bg_color = "#E3F2FD"
        icon = "ℹ️"
    
    st.markdown(f"""
    <div style="background-color: {bg_color}; padding: 15px; border-radius: 5px; border-left: 5px solid {color}; margin-bottom: 20px;">
        <h4 style="color: {color}; margin-top: 0;">{icon} {title}</h4>
        <p style="margin-bottom: 0;">{content}</p>
    </div>
    """, unsafe_allow_html=True)

def render_document_preview(document: Dict[str, Any]):
    """
    Render a preview of a document.
    
    Args:
        document: Document information dictionary
    """
    title = document.get("title", "Untitled Document")
    source = document.get("source", "Unknown source")
    content_preview = document.get("content", "")[:200] + "..." if len(document.get("content", "")) > 200 else document.get("content", "")
    
    st.markdown(f"""
    <div style="border: 1px solid #E5E7EB; border-radius: 5px; padding: 15px; margin-bottom: 15px;">
        <h4 style="margin-top: 0;">{title}</h4>
        <p style="color: #6B7280; font-size: 0.9em;">Source: {source}</p>
        <p>{content_preview}</p>
    </div>
    """, unsafe_allow_html=True)

def render_system_status(status: Dict[str, Any]):
    """
    Render the system status.
    
    Args:
        status: System status dictionary
    """
    st.sidebar.markdown("### System Status")
    
    # Documents status
    docs_loaded = status.get("documents_loaded", 0)
    docs_status = "✅" if docs_loaded > 0 else "❌"
    st.sidebar.markdown(f"Documents Loaded: {docs_status} ({docs_loaded} chunks)")
    
    # Embeddings status
    embeddings_status = "✅" if status.get("embeddings_created", False) else "❌"
    st.sidebar.markdown(f"Embeddings Created: {embeddings_status}")
    
    # Model status
    model_loaded = status.get("model_loaded", False)
    model_status = "✅" if model_loaded else "❌"
    model_name = status.get("model_name", "None")
    st.sidebar.markdown(f"Model Loaded: {model_status} ({model_name})")
    
    # System initialized
    system_initialized = status.get("system_initialized", False)
    system_status = "✅" if system_initialized else "❌"
    st.sidebar.markdown(f"System Initialized: {system_status}")

def render_welcome_message():
    """Render the welcome message for first-time users."""
    st.markdown("""
    <div style="background-color: #FFF8E1; padding: 20px; border-radius: 5px; border-left: 5px solid #FFB300; margin-bottom: 20px;">
        <h3 style="color: #F57C00; margin-top: 0;">👋 Welcome to the Sultanate Legal AI Assistant!</h3>
        <p>This AI assistant can answer your questions about Omani laws based solely on the legal documents it has been trained on.</p>
        <p><strong>To get started:</strong></p>
        <ol>
            <li>Add PDF files containing Omani legal documents to the <code>src/data</code> directory</li>
            <li>Use the sidebar to load documents and create embeddings</li>
            <li>Download a local LLM model and initialize the system</li>
            <li>Ask questions about Omani laws in the chat input below</li>
        </ol>
        <p><strong>Example questions:</strong></p>
        <ul>
            <li>"على ماذا ينص قانون الدفاع المدني العماني؟"</li>
            <li>"What are the provisions of the Omani Civil Defense Law?"</li>
            <li>"ما هي الإجراءات المتبعة في حالات الطوارئ حسب قانون الدفاع المدني؟"</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

def render_source_documents(documents: List[Dict[str, Any]]):
    """
    Render the source documents used to generate the answer.
    
    Args:
        documents: List of document information dictionaries
    """
    with st.expander("View Source Documents", expanded=False):
        if not documents:
            st.markdown("No source documents available.")
            return
        
        for i, doc in enumerate(documents):
            source = doc.get("source", "Unknown source")
            content = doc.get("content", "")
            
            st.markdown(f"**Source {i+1}:** {source}")
            st.text_area(f"Content {i+1}", content, height=150, key=f"source_{i}")
            st.markdown("---")


if __name__ == "__main__":
    # This is just for demonstration purposes
    st.set_page_config(page_title="UI Components Demo", layout="wide")
    
    render_header()
    
    st.markdown("### Chat Messages Demo")
    render_chat_message("user", "What is the punishment for theft according to Omani laws?")
    render_chat_message("assistant", "According to Article 279 of the Omani Penal Code, the punishment for theft is imprisonment for a period not less than three months and not exceeding three years, and a fine not less than 100 Omani Rials and not exceeding 500 Omani Rials.")
    
    st.markdown("### Info Boxes Demo")
    render_info_box("Information", "This is an information box.", "info")
    render_info_box("Success", "This is a success box.", "success")
    render_info_box("Warning", "This is a warning box.", "warning")
    render_info_box("Error", "This is an error box.", "error")
    
    st.markdown("### Document Preview Demo")
    render_document_preview({
        "title": "Omani Penal Code",
        "source": "penal_code_2018.pdf",
        "content": "Article 279: Whoever commits theft shall be punished with imprisonment for a period not less than three months and not exceeding three years, and a fine not less than 100 Omani Rials and not exceeding 500 Omani Rials."
    })
    
    st.markdown("### Welcome Message Demo")
    render_welcome_message()
