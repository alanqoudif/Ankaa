"""
UI components for document and image generation in the Legal AI Assistant.
"""

import streamlit as st
import base64
from typing import Dict, Any, Optional, Tuple, List, Callable

def render_document_generation_section(
    generate_document_callback: Callable,
    t: Callable[[str], str]
):
    """
    Render the document generation section in the UI.
    
    Args:
        generate_document_callback: Callback function to generate documents
        t: Translation function
    """
    st.markdown(f"### {t('document_generation_description')}")
    
    # Document type selection
    doc_type = st.selectbox(
        t("document_type"),
        options=["contract", "authorization"],
        format_func=lambda x: t(f"document_type_{x}")
    )
    
    # Document details
    if doc_type == "contract":
        render_contract_form(t)
    elif doc_type == "authorization":
        render_authorization_form(t)
    
    # Generate button
    if st.button(t("generate_document_button"), type="primary"):
        generate_document_callback(doc_type)

def render_contract_form(t: Callable[[str], str]):
    """Render form fields for contract generation."""
    # Contract type
    contract_type = st.selectbox(
        t("contract_type"),
        options=["employment", "rental", "service"],
        format_func=lambda x: t(f"contract_type_{x}")
    )
    
    # Contract parties
    col1, col2 = st.columns(2)
    with col1:
        first_party = st.text_input(t("first_party"), value=t("default_first_party"))
    with col2:
        second_party = st.text_input(t("second_party"), value=t("default_second_party"))
    
    # Contract details
    if contract_type == "employment":
        col1, col2 = st.columns(2)
        with col1:
            position = st.text_input(t("position"), value=t("default_position"))
            salary = st.number_input(t("salary"), min_value=0, value=1000)
        with col2:
            duration = st.text_input(t("duration"), value=t("default_duration"))
            start_date = st.date_input(t("start_date"))
    
    elif contract_type == "rental":
        col1, col2 = st.columns(2)
        with col1:
            property_desc = st.text_input(t("property_description"))
            rent_amount = st.number_input(t("rent_amount"), min_value=0, value=500)
        with col2:
            duration = st.text_input(t("duration"), value=t("default_duration"))
            start_date = st.date_input(t("start_date"))
    
    elif contract_type == "service":
        col1, col2 = st.columns(2)
        with col1:
            service_desc = st.text_area(t("service_description"), height=100)
            fee_amount = st.number_input(t("fee_amount"), min_value=0, value=500)
        with col2:
            duration = st.text_input(t("duration"), value=t("default_duration"))
            start_date = st.date_input(t("start_date"))

def render_authorization_form(t: Callable[[str], str]):
    """Render form fields for authorization document generation."""
    # Authorization parties
    col1, col2 = st.columns(2)
    with col1:
        authorizer = st.text_input(t("authorizer"), value=t("default_authorizer"))
    with col2:
        authorized = st.text_input(t("authorized"), value=t("default_authorized"))
    
    # Authorization details
    purpose = st.text_area(t("purpose"), height=100, value=t("default_purpose"))
    
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(t("start_date"))
    with col2:
        end_date = st.date_input(t("end_date"))

def render_download_section(
    pdf_data: Optional[bytes] = None,
    image_data: Optional[bytes] = None,
    zip_data: Optional[bytes] = None,
    document_type: str = "document",
    t: Callable[[str], str] = lambda x: x
):
    """
    Render the download section for generated documents and images.
    
    Args:
        pdf_data: PDF document data as bytes
        image_data: Image data as bytes
        zip_data: ZIP package data as bytes
        document_type: Type of document
        t: Translation function
    """
    if not any([pdf_data, image_data, zip_data]):
        return
    
    st.markdown(f"### {t('download_generated_files')}")
    
    col1, col2, col3 = st.columns(3)
    
    # PDF download
    if pdf_data:
        with col1:
            pdf_b64 = base64.b64encode(pdf_data).decode()
            pdf_filename = f"{document_type}_document.pdf"
            href = f'<a href="data:application/pdf;base64,{pdf_b64}" download="{pdf_filename}" class="download-button">{t("download_pdf")}</a>'
            st.markdown(href, unsafe_allow_html=True)
            
            # Preview button
            if st.button(t("preview_pdf"), key="preview_pdf"):
                st.markdown(f"### {t('pdf_preview')}")
                st.markdown(f'<iframe src="data:application/pdf;base64,{pdf_b64}" width="100%" height="500" type="application/pdf"></iframe>', unsafe_allow_html=True)
    
    # Image download
    if image_data:
        with col2:
            img_b64 = base64.b64encode(image_data).decode()
            img_filename = f"{document_type}_certificate.png"
            href = f'<a href="data:image/png;base64,{img_b64}" download="{img_filename}" class="download-button">{t("download_image")}</a>'
            st.markdown(href, unsafe_allow_html=True)
            
            # Preview
            if st.button(t("preview_image"), key="preview_image"):
                st.markdown(f"### {t('image_preview')}")
                st.image(image_data, caption=t(f"document_type_{document_type}"))
    
    # ZIP download
    if zip_data:
        with col3:
            zip_b64 = base64.b64encode(zip_data).decode()
            zip_filename = f"{document_type}_package.zip"
            href = f'<a href="data:application/zip;base64,{zip_b64}" download="{zip_filename}" class="download-button">{t("download_zip")}</a>'
            st.markdown(href, unsafe_allow_html=True)
    
    # Add some CSS for the download buttons
    st.markdown("""
    <style>
    .download-button {
        display: inline-block;
        padding: 0.5em 1em;
        color: white;
        background-color: #1E3A8A;
        text-align: center;
        text-decoration: none;
        font-weight: bold;
        border-radius: 4px;
        margin: 0.5em 0;
        transition: background-color 0.3s;
    }
    .download-button:hover {
        background-color: #2E4A9A;
    }
    </style>
    """, unsafe_allow_html=True)

def render_document_preview(pdf_data: bytes, t: Callable[[str], str] = lambda x: x):
    """
    Render a preview of the generated PDF document.
    
    Args:
        pdf_data: PDF document data as bytes
        t: Translation function
    """
    st.markdown(f"### {t('document_preview')}")
    
    # Convert PDF to base64
    pdf_b64 = base64.b64encode(pdf_data).decode()
    
    # Display PDF in an iframe
    st.markdown(f'<iframe src="data:application/pdf;base64,{pdf_b64}" width="100%" height="500" type="application/pdf"></iframe>', unsafe_allow_html=True)

def render_image_preview(image_data: bytes, caption: str = "", t: Callable[[str], str] = lambda x: x):
    """
    Render a preview of the generated image.
    
    Args:
        image_data: Image data as bytes
        caption: Image caption
        t: Translation function
    """
    st.markdown(f"### {t('image_preview')}")
    st.image(image_data, caption=caption)

def collect_form_data() -> Dict[str, Any]:
    """
    Collect form data from the UI.
    
    Returns:
        Dictionary containing form data
    """
    data = {}
    
    # Get form values from session state
    for key in st.session_state:
        if key.startswith('form_'):
            # Extract the actual field name by removing the 'form_' prefix
            field_name = key[5:]
            data[field_name] = st.session_state[key]
    
    return data
