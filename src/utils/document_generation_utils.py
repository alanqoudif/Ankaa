"""
Utility functions for document generation in the Legal AI Assistant.
"""

import os
import io
import datetime
import importlib.util
from typing import Dict, Any, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
import tempfile
import zipfile

# Check for available PDF generation libraries
PDF_GENERATORS = []

# Try to import weasyprint
if importlib.util.find_spec("weasyprint") is not None:
    try:
        from weasyprint import HTML, CSS
        PDF_GENERATORS.append("weasyprint")
    except ImportError:
        pass

# Try to import reportlab
if importlib.util.find_spec("reportlab") is not None:
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        PDF_GENERATORS.append("reportlab")
    except ImportError:
        pass

# Try to import pdfkit
if importlib.util.find_spec("pdfkit") is not None:
    try:
        import pdfkit
        PDF_GENERATORS.append("pdfkit")
    except ImportError:
        pass

class DocumentGenerator:
    """Class for generating legal documents and certificates."""
    
    def __init__(self, templates_dir: str = None):
        """
        Initialize the document generator.
        
        Args:
            templates_dir: Directory containing document templates
        """
        self.templates_dir = templates_dir or os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "templates")
        os.makedirs(self.templates_dir, exist_ok=True)
        
    def generate_legal_document(self, document_type: str, content: Dict[str, Any]) -> bytes:
        """
        Generate a legal document as PDF.
        
        Args:
            document_type: Type of document to generate (e.g., 'contract', 'authorization')
            content: Dictionary containing document content
            
        Returns:
            PDF document as bytes
        """
        # Create HTML content based on document type and content
        html_content = self._create_document_html(document_type, content)
        
        # Convert HTML to PDF
        pdf_bytes = self._html_to_pdf(html_content)
        return pdf_bytes
    
    def generate_document_image(self, document_type: str, content: Dict[str, Any], 
                               width: int = 800, height: int = 1100) -> bytes:
        """
        Generate an image representing a document (e.g., certificate, contract cover).
        
        Args:
            document_type: Type of document image to generate
            content: Dictionary containing image content
            width: Image width
            height: Image height
            
        Returns:
            Image as bytes
        """
        # Create a new image with white background
        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image)
        
        # Try to load fonts
        try:
            title_font = ImageFont.truetype("Arial", 36)
            header_font = ImageFont.truetype("Arial", 24)
            body_font = ImageFont.truetype("Arial", 16)
        except IOError:
            # Fallback to default font if Arial is not available
            title_font = ImageFont.load_default()
            header_font = ImageFont.load_default()
            body_font = ImageFont.load_default()
        
        # Draw border
        draw.rectangle([(20, 20), (width-20, height-20)], outline='black', width=2)
        
        # Draw decorative header
        draw.rectangle([(20, 20), (width-20, 100)], fill='#1E3A8A')
        
        # Add title
        title = content.get('title', 'Legal Document')
        draw.text((width//2, 60), title, fill='white', font=title_font, anchor='mm')
        
        # Add document type
        doc_type = content.get('document_type', document_type.capitalize())
        draw.text((width//2, 150), doc_type, fill='black', font=header_font, anchor='mm')
        
        # Add user name if available
        if 'user_name' in content:
            draw.text((width//2, 200), f"Name: {content['user_name']}", fill='black', font=body_font, anchor='mm')
        
        # Add date
        date_str = content.get('date', datetime.datetime.now().strftime("%Y-%m-%d"))
        draw.text((width//2, 240), f"Date: {date_str}", fill='black', font=body_font, anchor='mm')
        
        # Add official seal/logo
        self._draw_official_seal(draw, width//2, height-150, 100)
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()
    
    def create_document_package(self, document_type: str, content: Dict[str, Any]) -> Tuple[bytes, bytes, bytes]:
        """
        Create a complete document package including PDF, image, and ZIP.
        
        Args:
            document_type: Type of document to generate
            content: Dictionary containing document content
            
        Returns:
            Tuple of (pdf_bytes, image_bytes, zip_bytes)
        """
        # Generate PDF
        pdf_bytes = self.generate_legal_document(document_type, content)
        
        # Generate image
        image_bytes = self.generate_document_image(document_type, content)
        
        # Create ZIP package
        zip_bytes = self._create_zip_package(pdf_bytes, image_bytes, document_type)
        
        return pdf_bytes, image_bytes, zip_bytes
    
    def _create_document_html(self, document_type: str, content: Dict[str, Any]) -> str:
        """Create HTML content for the document based on type and content."""
        # Basic HTML structure
        html = f"""
        <!DOCTYPE html>
        <html dir="rtl">
        <head>
            <meta charset="UTF-8">
            <title>{content.get('title', 'Legal Document')}</title>
            <style>
                @page {{
                    size: A4;
                    margin: 2cm;
                }}
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.5;
                    direction: rtl;
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 2cm;
                }}
                .title {{
                    font-size: 24pt;
                    font-weight: bold;
                    color: #1E3A8A;
                    margin-bottom: 0.5cm;
                }}
                .subtitle {{
                    font-size: 14pt;
                    margin-bottom: 1cm;
                }}
                .section-title {{
                    font-size: 14pt;
                    font-weight: bold;
                    margin-top: 1cm;
                    margin-bottom: 0.5cm;
                    color: #1E3A8A;
                }}
                .content {{
                    font-size: 12pt;
                }}
                .signature {{
                    margin-top: 2cm;
                    page-break-inside: avoid;
                }}
                .signature-line {{
                    border-top: 1px solid black;
                    width: 7cm;
                    margin-top: 1.5cm;
                }}
                .date {{
                    margin-top: 0.5cm;
                    font-style: italic;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 1cm 0;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: right;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
            </style>
        </head>
        <body>
        """
        
        # Add header
        html += f"""
        <div class="header">
            <div class="title">{content.get('title', 'Legal Document')}</div>
            <div class="subtitle">{content.get('subtitle', '')}</div>
        </div>
        """
        
        # Add content based on document type
        if document_type == 'contract':
            html += self._create_contract_html(content)
        elif document_type == 'authorization':
            html += self._create_authorization_html(content)
        else:
            # Generic document
            html += self._create_generic_document_html(content)
        
        # Add date and signature
        date_str = content.get('date', datetime.datetime.now().strftime("%Y-%m-%d"))
        html += f"""
        <div class="signature">
            <div class="date">تاريخ: {date_str}</div>
            <table style="width: 100%; border: none;">
                <tr style="border: none;">
                    <td style="border: none; width: 50%;">
                        <p>توقيع الطرف الأول:</p>
                        <div class="signature-line"></div>
                        <p>{content.get('first_party', '')}</p>
                    </td>
                    <td style="border: none; width: 50%;">
                        <p>توقيع الطرف الثاني:</p>
                        <div class="signature-line"></div>
                        <p>{content.get('second_party', '')}</p>
                    </td>
                </tr>
            </table>
        </div>
        """
        
        # Close HTML
        html += """
        </body>
        </html>
        """
        
        return html
    
    def _create_contract_html(self, content: Dict[str, Any]) -> str:
        """Create HTML content for a contract."""
        html = ""
        
        # Parties section
        html += """
        <div class="section-title">الأطراف</div>
        <div class="content">
        """
        
        first_party = content.get('first_party', 'الطرف الأول')
        second_party = content.get('second_party', 'الطرف الثاني')
        
        html += f"""
            <p><strong>الطرف الأول:</strong> {first_party}</p>
            <p><strong>الطرف الثاني:</strong> {second_party}</p>
        </div>
        """
        
        # Terms section
        html += """
        <div class="section-title">بنود العقد</div>
        <div class="content">
        """
        
        # Add terms
        terms = content.get('terms', [])
        if terms:
            html += "<ol>"
            for term in terms:
                html += f"<li>{term}</li>"
            html += "</ol>"
        else:
            # Default terms for employment contract
            if content.get('contract_type') == 'employment':
                salary = content.get('salary', '0')
                duration = content.get('duration', '1 سنة')
                position = content.get('position', 'موظف')
                
                html += f"""
                <ol>
                    <li>يعين الطرف الأول الطرف الثاني في وظيفة {position} وفقاً للشروط والأحكام المنصوص عليها في هذا العقد.</li>
                    <li>مدة هذا العقد {duration} تبدأ من تاريخ توقيع هذا العقد.</li>
                    <li>يتقاضى الطرف الثاني راتباً شهرياً قدره {salary} ريال عماني.</li>
                    <li>يخضع هذا العقد لأحكام قانون العمل العماني.</li>
                    <li>ساعات العمل 8 ساعات يومياً، 5 أيام في الأسبوع.</li>
                    <li>يستحق الطرف الثاني إجازة سنوية مدتها 30 يوماً مدفوعة الراتب.</li>
                    <li>يلتزم الطرف الثاني بالحفاظ على سرية المعلومات الخاصة بالطرف الأول.</li>
                    <li>يحق للطرف الأول إنهاء هذا العقد في حالة مخالفة الطرف الثاني لأي من بنود هذا العقد.</li>
                </ol>
                """
        
        html += "</div>"
        return html
    
    def _create_authorization_html(self, content: Dict[str, Any]) -> str:
        """Create HTML content for an authorization document."""
        html = ""
        
        authorizer = content.get('authorizer', 'المفوض')
        authorized = content.get('authorized', 'المفوض إليه')
        purpose = content.get('purpose', 'الغرض من التفويض')
        
        html += f"""
        <div class="content">
            <p>أنا الموقع أدناه، {authorizer}، أفوض السيد/السيدة {authorized} للقيام بما يلي:</p>
            <p>{purpose}</p>
            
            <p>وهذا التفويض ساري المفعول من تاريخ {content.get('start_date', 'توقيع هذا المستند')} 
            إلى تاريخ {content.get('end_date', 'انتهاء الغرض من التفويض')}.</p>
            
            <p>وأتحمل كامل المسؤولية القانونية عن هذا التفويض.</p>
        </div>
        """
        
        return html
    
    def _create_generic_document_html(self, content: Dict[str, Any]) -> str:
        """Create HTML content for a generic document."""
        html = ""
        
        # Main content
        main_content = content.get('content', '')
        if isinstance(main_content, list):
            html += "<div class='content'>"
            for paragraph in main_content:
                html += f"<p>{paragraph}</p>"
            html += "</div>"
        else:
            html += f"<div class='content'><p>{main_content}</p></div>"
        
        return html
    
    def _html_to_pdf(self, html_content: str) -> bytes:
        """Convert HTML content to PDF using available libraries."""
        pdf_bytes = io.BytesIO()
        
        # Try using weasyprint first
        if "weasyprint" in PDF_GENERATORS:
            try:
                from weasyprint import HTML
                HTML(string=html_content).write_pdf(pdf_bytes)
                return pdf_bytes.getvalue()
            except Exception as e:
                print(f"Error using weasyprint: {e}")
        
        # Try using pdfkit next
        if "pdfkit" in PDF_GENERATORS:
            try:
                import pdfkit
                # Save HTML to a temporary file
                with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as temp_html:
                    temp_html.write(html_content.encode('utf-8'))
                    temp_html_path = temp_html.name
                
                # Convert HTML to PDF
                try:
                    pdf_data = pdfkit.from_file(temp_html_path, False)
                    os.unlink(temp_html_path)  # Delete the temporary file
                    return pdf_data
                except Exception as e:
                    os.unlink(temp_html_path)  # Delete the temporary file
                    print(f"Error using pdfkit: {e}")
            except Exception as e:
                print(f"Error using pdfkit: {e}")
        
        # Try using reportlab as a last resort
        if "reportlab" in PDF_GENERATORS:
            try:
                from reportlab.pdfgen import canvas
                from reportlab.lib.pagesizes import A4
                from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                
                # Create a simple PDF with basic text
                doc = SimpleDocTemplate(pdf_bytes, pagesize=A4)
                styles = getSampleStyleSheet()
                
                # Add right-to-left support for Arabic text
                rtl_style = ParagraphStyle(
                    'RTL',
                    parent=styles['Normal'],
                    alignment=2,  # Right alignment
                    fontName='Helvetica',
                    fontSize=12
                )
                
                # Extract text from HTML (very basic approach)
                import re
                text_content = re.sub('<.*?>', ' ', html_content)
                text_content = re.sub('\s+', ' ', text_content).strip()
                
                # Create document content
                content = []
                paragraphs = text_content.split('\n')
                for para in paragraphs:
                    if para.strip():
                        content.append(Paragraph(para, rtl_style))
                        content.append(Spacer(1, 12))
                
                # Build the PDF
                doc.build(content)
                return pdf_bytes.getvalue()
            except Exception as e:
                print(f"Error using reportlab: {e}")
        
        # If all methods fail, create a simple text-based PDF with reportlab
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import A4
            
            c = canvas.Canvas(pdf_bytes, pagesize=A4)
            width, height = A4
            
            # Add a title
            c.setFont("Helvetica-Bold", 16)
            c.drawCentredString(width/2, height-50, "Legal Document")
            
            # Add a message about PDF generation
            c.setFont("Helvetica", 12)
            c.drawCentredString(width/2, height-80, "PDF generation libraries not available")
            c.drawCentredString(width/2, height-100, "Please install weasyprint, pdfkit, or reportlab")
            
            c.save()
            return pdf_bytes.getvalue()
        except Exception as e:
            # Last resort: Return an empty PDF
            print(f"Failed to generate PDF: {e}")
            return b'%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj 2 0 obj<</Type/Pages/Count 1/Kids[3 0 R]>>endobj 3 0 obj<</Type/Page/MediaBox[0 0 595 842]/Parent 2 0 R/Resources<<>>>>endobj\nxref\n0 4\n0000000000 65535 f\n0000000009 00000 n\n0000000056 00000 n\n0000000111 00000 n\n\ntrailer<</Size 4/Root 1 0 R>>\nstartxref\n190\n%%EOF'
    
    def _draw_official_seal(self, draw: ImageDraw, x: int, y: int, size: int):
        """Draw an official-looking seal on the image."""
        # Outer circle
        draw.ellipse([(x-size, y-size), (x+size, y+size)], outline='#1E3A8A', width=3)
        
        # Inner circle
        inner_size = size * 0.8
        draw.ellipse([(x-inner_size, y-inner_size), (x+inner_size, y+inner_size)], outline='#1E3A8A', width=2)
        
        # Center text
        try:
            seal_font = ImageFont.truetype("Arial", 16)
        except IOError:
            seal_font = ImageFont.load_default()
            
        draw.text((x, y-10), "سلطنة عمان", fill='#1E3A8A', font=seal_font, anchor='mm')
        draw.text((x, y+10), "وثيقة رسمية", fill='#1E3A8A', font=seal_font, anchor='mm')
    
    def _create_zip_package(self, pdf_bytes: bytes, image_bytes: bytes, document_type: str) -> bytes:
        """Create a ZIP package containing the PDF and image."""
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # Add PDF
            zip_file.writestr(f"{document_type}_document.pdf", pdf_bytes)
            
            # Add image
            zip_file.writestr(f"{document_type}_certificate.png", image_bytes)
            
            # Add a simple README
            readme_content = f"""
            {document_type.capitalize()} Document Package
            ============================
            
            This package contains:
            1. {document_type}_document.pdf - The legal document in PDF format
            2. {document_type}_certificate.png - Certificate image
            
            Generated on: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            """
            zip_file.writestr("README.txt", readme_content)
        
        return zip_buffer.getvalue()

# Helper function to extract document content from user query
def extract_document_content_from_query(query: str) -> Tuple[str, Dict[str, Any]]:
    """
    Extract document type and content from a user query.
    
    Args:
        query: User query string
        
    Returns:
        Tuple of (document_type, content_dict)
    """
    # Default values
    document_type = "contract"
    content = {
        "title": "وثيقة قانونية",
        "date": datetime.datetime.now().strftime("%Y-%m-%d")
    }
    
    # Check for document type
    if "عقد" in query or "contract" in query.lower():
        document_type = "contract"
        content["title"] = "عقد"
        
        # Check for employment contract
        if "عمل" in query or "employment" in query.lower() or "توظيف" in query:
            content["contract_type"] = "employment"
            content["title"] = "عقد عمل"
            
            # Extract position
            position_matches = {
                "مهندس": "مهندس",
                "engineer": "مهندس",
                "محاسب": "محاسب",
                "accountant": "محاسب",
                "مدير": "مدير",
                "manager": "مدير",
                "موظف": "موظف",
                "employee": "موظف"
            }
            
            for key, value in position_matches.items():
                if key in query.lower():
                    content["position"] = value
                    break
            
            # Extract salary
            import re
            salary_match = re.search(r'(\d+)\s*(ريال|ر\.ع\.|omr|rial)', query, re.IGNORECASE)
            if salary_match:
                content["salary"] = salary_match.group(1)
            
            # Extract duration
            duration_matches = {
                "سنة": "سنة واحدة",
                "سنتين": "سنتين",
                "سنوات": "سنوات",
                "year": "سنة واحدة",
                "years": "سنوات",
                "شهر": "شهر",
                "أشهر": "أشهر",
                "month": "شهر",
                "months": "أشهر"
            }
            
            for key, value in duration_matches.items():
                if key in query.lower():
                    # Try to find a number before the duration word
                    num_match = re.search(r'(\d+)\s*' + key, query)
                    if num_match:
                        content["duration"] = f"{num_match.group(1)} {value}"
                    else:
                        content["duration"] = value
                    break
    
    elif "تفويض" in query or "authorization" in query.lower():
        document_type = "authorization"
        content["title"] = "تفويض"
        
        # Extract purpose
        if "لغرض" in query or "purpose" in query.lower():
            purpose_match = re.search(r'لغرض\s*(.+?)(?:\.|$)', query)
            if purpose_match:
                content["purpose"] = purpose_match.group(1)
    
    # Extract names
    # This is a simplified approach - in a real system, you'd use NER or more sophisticated methods
    name_indicators = [
        "اسم", "name", "المدعو", "السيد", "السيدة", "mr", "mrs", "ms"
    ]
    
    for indicator in name_indicators:
        if indicator in query.lower():
            name_match = re.search(r'' + indicator + r'\s+([^\s,]+(?:\s+[^\s,]+){0,3})', query, re.IGNORECASE)
            if name_match:
                if "user_name" not in content:
                    content["user_name"] = name_match.group(1)
                    content["first_party"] = name_match.group(1)
                break
    
    return document_type, content
