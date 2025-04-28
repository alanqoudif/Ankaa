"""
Utility functions for legal case analysis and report generation in the Legal AI Assistant.
This module provides functionality for Level 5 - AI Reports and Case Study Creation.
"""

import os
import io
import datetime
import re
from typing import Dict, Any, List, Tuple, Optional
import tempfile

from utils.document_generation_utils import DocumentGenerator


class LegalCaseAnalyzer:
    """Class for analyzing legal cases and generating comprehensive reports."""
    
    def __init__(self, retriever=None, qa_chain=None):
        """
        Initialize the legal case analyzer.
        
        Args:
            retriever: Document retriever for finding relevant legal information
            qa_chain: QA chain for answering questions about the case
        """
        self.retriever = retriever
        self.qa_chain = qa_chain
        self.document_generator = DocumentGenerator()
        
    def analyze_case(self, scenario: str) -> Dict[str, Any]:
        """
        Analyze a legal scenario and identify relevant laws and implications.
        
        Args:
            scenario: Description of the legal scenario to analyze
            
        Returns:
            Dictionary containing analysis results
        """
        # Extract key elements from the scenario
        case_elements = self._extract_case_elements(scenario)
        
        # Retrieve relevant legal documents
        relevant_docs = self._retrieve_relevant_documents(scenario, case_elements)
        
        # Analyze legal implications
        legal_analysis = self._analyze_legal_implications(scenario, case_elements, relevant_docs)
        
        # Prepare final analysis results
        analysis_results = {
            "scenario": scenario,
            "case_elements": case_elements,
            "relevant_laws": legal_analysis["relevant_laws"],
            "legal_implications": legal_analysis["implications"],
            "conclusion": legal_analysis["conclusion"],
            "references": [doc.metadata for doc in relevant_docs],
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return analysis_results
    
    def generate_case_report(self, analysis_results: Dict[str, Any]) -> bytes:
        """
        Generate a comprehensive PDF report for the case analysis.
        
        Args:
            analysis_results: Results from analyze_case method
            
        Returns:
            PDF report as bytes
        """
        # Prepare content for the report
        content = self._prepare_report_content(analysis_results)
        
        # Generate PDF using DocumentGenerator
        pdf_bytes = self.document_generator.generate_legal_document("case_report", content)
        
        return pdf_bytes
    
    def _extract_case_elements(self, scenario: str) -> Dict[str, Any]:
        """Extract key elements from the scenario description."""
        elements = {
            "actors": [],
            "actions": [],
            "locations": [],
            "legal_domains": []
        }
        
        # Identify potential legal domains
        legal_domains = {
            "استثمار": "investment_law",
            "investment": "investment_law",
            "ضرائب": "tax_law",
            "tax": "tax_law",
            "عمل": "labor_law",
            "employment": "labor_law",
            "labor": "labor_law",
            "تجارة": "commercial_law",
            "commerce": "commercial_law",
            "commercial": "commercial_law",
            "عقارات": "real_estate_law",
            "real estate": "real_estate_law",
            "جنائي": "criminal_law",
            "criminal": "criminal_law",
            "مدني": "civil_law",
            "civil": "civil_law",
            "أسرة": "family_law",
            "family": "family_law",
            "مالية": "financial_law",
            "financial": "financial_law",
            "بنك": "banking_law",
            "bank": "banking_law",
            "banking": "banking_law",
            "شركة": "company_law",
            "company": "company_law",
            "corporate": "company_law",
            "تأمين": "insurance_law",
            "insurance": "insurance_law",
            "ملكية فكرية": "intellectual_property_law",
            "intellectual property": "intellectual_property_law",
            "بيئة": "environmental_law",
            "environmental": "environmental_law",
            "جمارك": "customs_law",
            "customs": "customs_law"
        }
        
        # Actor identification patterns
        actor_patterns = [
            r'مواطن',
            r'شخص',
            r'فرد',
            r'شركة',
            r'مؤسسة',
            r'مستثمر',
            r'موظف',
            r'صاحب عمل',
            r'مالك',
            r'مستأجر',
            r'بائع',
            r'مشتري',
            r'citizen',
            r'person',
            r'individual',
            r'company',
            r'institution',
            r'investor',
            r'employee',
            r'employer',
            r'owner',
            r'tenant',
            r'seller',
            r'buyer'
        ]
        
        # Action identification patterns
        action_patterns = [
            r'استثمر',
            r'اشترى',
            r'باع',
            r'استأجر',
            r'أجّر',
            r'وقّع',
            r'تعاقد',
            r'خالف',
            r'ارتكب',
            r'أنشأ',
            r'أسس',
            r'invested',
            r'purchased',
            r'sold',
            r'rented',
            r'leased',
            r'signed',
            r'contracted',
            r'violated',
            r'committed',
            r'established',
            r'founded'
        ]
        
        # Location identification patterns
        location_patterns = [
            r'في عمان',
            r'خارج عمان',
            r'داخل السلطنة',
            r'خارج السلطنة',
            r'في الخارج',
            r'محلياً',
            r'دولياً',
            r'in Oman',
            r'outside Oman',
            r'within the Sultanate',
            r'outside the Sultanate',
            r'abroad',
            r'locally',
            r'internationally'
        ]
        
        # Extract legal domains
        for key, domain in legal_domains.items():
            if key in scenario.lower():
                if domain not in elements["legal_domains"]:
                    elements["legal_domains"].append(domain)
        
        # Extract actors
        for pattern in actor_patterns:
            if re.search(pattern, scenario, re.IGNORECASE):
                actor = re.search(pattern, scenario, re.IGNORECASE).group(0)
                if actor not in elements["actors"]:
                    elements["actors"].append(actor)
        
        # Extract actions
        for pattern in action_patterns:
            if re.search(pattern, scenario, re.IGNORECASE):
                action = re.search(pattern, scenario, re.IGNORECASE).group(0)
                if action not in elements["actions"]:
                    elements["actions"].append(action)
        
        # Extract locations
        for pattern in location_patterns:
            if re.search(pattern, scenario, re.IGNORECASE):
                location = re.search(pattern, scenario, re.IGNORECASE).group(0)
                if location not in elements["locations"]:
                    elements["locations"].append(location)
        
        # If no domains were identified, add a generic one
        if not elements["legal_domains"]:
            elements["legal_domains"].append("general_law")
        
        return elements
    
    def _retrieve_relevant_documents(self, scenario: str, case_elements: Dict[str, Any]) -> List[Any]:
        """Retrieve relevant legal documents for the scenario."""
        if not self.retriever:
            return []
        
        # Create a focused query based on the scenario and extracted elements
        domains_text = " ".join(case_elements["legal_domains"])
        focused_query = f"{scenario} {domains_text}"
        
        # Retrieve relevant documents with a higher k to ensure comprehensive coverage
        documents = self.retriever.retrieve(focused_query, k=15)
        
        return documents
    
    def _analyze_legal_implications(self, scenario: str, case_elements: Dict[str, Any], 
                                   relevant_docs: List[Any]) -> Dict[str, Any]:
        """Analyze legal implications based on the scenario and relevant documents."""
        if not self.qa_chain:
            # Fallback analysis if no QA chain is available
            return self._fallback_analysis(scenario, case_elements, relevant_docs)
        
        # Prepare comprehensive questions for the QA chain
        questions = [
            f"What are the specific Omani laws and articles that apply to this scenario: {scenario}? Please list them with their official names and article numbers.",
            f"What are the detailed legal implications for each party involved in this scenario: {scenario}? Explain the rights, obligations, and potential legal consequences for each actor.",
            f"What is the legal conclusion or outcome for this scenario: {scenario}? Provide a comprehensive analysis based solely on Omani law.",
            f"Are there any penalties, fines, or legal sanctions that might apply in this scenario: {scenario}? If so, specify the exact amounts or ranges according to Omani law.",
            f"What legal procedures or remedies are available to the parties in this scenario: {scenario}? Describe the process according to Omani legal system."
        ]
        
        # Get answers from the QA chain
        answers = []
        for question in questions:
            answer = self.qa_chain.run(question=question, documents=relevant_docs)
            answers.append(answer)
        
        # Extract relevant laws, implications, and conclusion
        relevant_laws = self._extract_laws_from_answer(answers[0], relevant_docs)
        implications = answers[1]
        conclusion = answers[2]
        penalties = answers[3]
        procedures = answers[4]
        
        # Create a structured legal analysis
        legal_analysis = {
            "relevant_laws": relevant_laws,
            "implications": implications,
            "penalties": penalties,
            "procedures": procedures,
            "conclusion": conclusion
        }
        
        return legal_analysis
    
    def _fallback_analysis(self, scenario: str, case_elements: Dict[str, Any], 
                          relevant_docs: List[Any]) -> Dict[str, Any]:
        """Provide a fallback analysis when QA chain is not available."""
        # Extract potential laws from document metadata
        relevant_laws = []
        for doc in relevant_docs:
            law_name = doc.metadata.get("source", "").split("/")[-1].replace(".pdf", "")
            if law_name and law_name not in [law["name"] for law in relevant_laws]:
                relevant_laws.append({
                    "name": law_name,
                    "articles": [{"number": "N/A", "content": doc.page_content}]
                })
        
        # Generate generic implications based on domains
        implications = "Based on the provided scenario, there may be legal implications related to "
        implications += ", ".join([domain.replace("_", " ") for domain in case_elements["legal_domains"]])
        implications += ". Please consult the relevant laws and regulations for specific details."
        
        # Generic conclusion
        conclusion = "To determine the exact legal outcome, please consult with a qualified legal professional."
        
        return {
            "relevant_laws": relevant_laws,
            "implications": implications,
            "conclusion": conclusion
        }
    
    def _extract_laws_from_answer(self, answer: str, relevant_docs: List[Any]) -> List[Dict[str, Any]]:
        """Extract structured law information from the answer and relevant documents."""
        laws = []
        
        # Extract law names and article numbers from the answer
        law_pattern = r"(?:قانون|law|code)\s+([^\n,.]+)"
        article_pattern = r"(?:المادة|article)\s+(\d+)"
        
        law_matches = re.finditer(law_pattern, answer, re.IGNORECASE)
        article_matches = re.finditer(article_pattern, answer, re.IGNORECASE)
        
        # Extract law names
        law_names = [match.group(1).strip() for match in law_matches]
        
        # Extract article numbers
        article_numbers = [match.group(1).strip() for match in article_matches]
        
        # If no laws or articles were extracted, try to get them from document metadata
        if not law_names:
            for doc in relevant_docs:
                law_name = doc.metadata.get("source", "").split("/")[-1].replace(".pdf", "")
                if law_name and law_name not in [law["name"] for law in laws]:
                    laws.append({
                        "name": law_name,
                        "articles": []
                    })
        else:
            # Create law entries
            for law_name in law_names:
                if law_name not in [law["name"] for law in laws]:
                    laws.append({
                        "name": law_name,
                        "articles": []
                    })
        
        # Add articles to laws
        for article_number in article_numbers:
            # Find the article content in relevant documents
            article_content = self._find_article_content(article_number, relevant_docs)
            
            # Add to the first law (simplified approach)
            if laws:
                laws[0]["articles"].append({
                    "number": article_number,
                    "content": article_content
                })
        
        return laws
    
    def _find_article_content(self, article_number: str, documents: List[Any]) -> str:
        """Find the content of a specific article in the documents."""
        article_patterns = [
            rf"المادة\s+{article_number}\s*[:\.]\s*([^\n]+)",
            rf"Article\s+{article_number}\s*[:\.]\s*([^\n]+)"
        ]
        
        for doc in documents:
            for pattern in article_patterns:
                match = re.search(pattern, doc.page_content, re.IGNORECASE)
                if match:
                    return match.group(1).strip()
        
        # If no specific content is found, return a placeholder
        return f"Article {article_number} content not found in the provided documents."
    
    def _prepare_report_content(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare content for the case report."""
        # Format the scenario
        scenario = analysis_results["scenario"]
        
        # Format case elements if available
        case_elements_content = ""
        if "case_elements" in analysis_results and analysis_results["case_elements"]:
            elements = analysis_results["case_elements"]
            
            if elements.get("actors"):
                case_elements_content += "الأطراف المعنية: " + "، ".join(elements["actors"]) + "\n\n"
            
            if elements.get("actions"):
                case_elements_content += "الأفعال: " + "، ".join(elements["actions"]) + "\n\n"
            
            if elements.get("locations"):
                case_elements_content += "المواقع: " + "، ".join(elements["locations"]) + "\n\n"
            
            if elements.get("legal_domains"):
                domains = [domain.replace("_", " ").title() for domain in elements["legal_domains"]]
                case_elements_content += "المجالات القانونية: " + "، ".join(domains) + "\n\n"
        
        # Format relevant laws
        relevant_laws_content = []
        for law in analysis_results["relevant_laws"]:
            law_content = f"**{law['name']}**\n\n"
            for article in law["articles"]:
                law_content += f"المادة {article['number']}: {article['content']}\n\n"
            relevant_laws_content.append(law_content)
        
        # Format legal implications
        implications = analysis_results.get("implications", "")
        
        # Format penalties if available
        penalties = analysis_results.get("penalties", "")
        
        # Format legal procedures if available
        procedures = analysis_results.get("procedures", "")
        
        # Format conclusion
        conclusion = analysis_results.get("conclusion", "")
        
        # Format references
        references = []
        for ref in analysis_results.get("references", []):
            source = ref.get("source", "Unknown")
            page = ref.get("page", "N/A")
            references.append(f"{source} (صفحة {page})")
        
        # Prepare the content sections
        content_sections = [
            f"**السيناريو:**\n\n{scenario}"
        ]
        
        # Add case elements if available
        if case_elements_content:
            content_sections.append(f"**عناصر القضية:**\n\n{case_elements_content}")
        
        # Add relevant laws
        content_sections.append(f"**القوانين والمواد ذات الصلة:**\n\n" + "\n".join(relevant_laws_content))
        
        # Add implications
        content_sections.append(f"**التحليل القانوني والآثار المترتبة:**\n\n{implications}")
        
        # Add penalties if available
        if penalties:
            content_sections.append(f"**العقوبات والغرامات المحتملة:**\n\n{penalties}")
        
        # Add procedures if available
        if procedures:
            content_sections.append(f"**الإجراءات القانونية المتاحة:**\n\n{procedures}")
        
        # Add conclusion
        content_sections.append(f"**الخلاصة:**\n\n{conclusion}")
        
        # Add references
        if references:
            content_sections.append(f"**المراجع:**\n\n" + "\n".join(references))
        
        # Prepare the content dictionary
        content = {
            "title": "تقرير تحليل قانوني",
            "subtitle": "تحليل قانوني لسيناريو قانوني",
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "content": content_sections
        }
        
        return content


# Add case report template to DocumentGenerator
def add_case_report_template_to_document_generator():
    """Add case report template to DocumentGenerator class."""
    # This function extends the DocumentGenerator._create_document_html method
    # to handle case report document type
    
    original_create_document_html = DocumentGenerator._create_document_html
    
    def extended_create_document_html(self, document_type: str, content: Dict[str, Any]) -> str:
        """Extended version of _create_document_html that handles case reports."""
        if document_type == "case_report":
            return create_case_report_html(content)
        else:
            return original_create_document_html(self, document_type, content)
    
    # Replace the original method with the extended one
    DocumentGenerator._create_document_html = extended_create_document_html


def create_case_report_html(content: Dict[str, Any]) -> str:
    """Create HTML content for a case report."""
    # Basic HTML structure with RTL support and enhanced styling
    html = f"""
    <!DOCTYPE html>
    <html dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>{content.get('title', 'تقرير تحليل قانوني')}</title>
        <style>
            @page {{
                size: A4;
                margin: 2cm;
                @top-center {{
                    content: "المساعد القانوني الذكي لسلطنة عمان";
                    font-size: 9pt;
                    color: #666;
                }}
                @bottom-center {{
                    content: "صفحة " counter(page) " من " counter(pages);
                    font-size: 9pt;
                }}
            }}
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                direction: rtl;
                color: #333;
                margin: 0;
                padding: 0;
                background-color: #fff;
            }}
            .header {{
                text-align: center;
                margin-bottom: 2cm;
                border-bottom: 2px solid #1E3A8A;
                padding-bottom: 0.5cm;
            }}
            .title {{
                font-size: 26pt;
                font-weight: bold;
                color: #1E3A8A;
                margin-bottom: 0.5cm;
            }}
            .subtitle {{
                font-size: 16pt;
                margin-bottom: 1cm;
                color: #555;
            }}
            .section {{
                margin-bottom: 1.5cm;
            }}
            .section-title {{
                font-size: 16pt;
                font-weight: bold;
                margin-top: 1cm;
                margin-bottom: 0.5cm;
                color: #1E3A8A;
                border-bottom: 1px solid #ccc;
                padding-bottom: 0.2cm;
            }}
            .content {{
                font-size: 12pt;
            }}
            .footer {{
                margin-top: 2cm;
                text-align: center;
                font-size: 10pt;
                color: #666;
                border-top: 1px solid #ccc;
                padding-top: 0.5cm;
            }}
            .signature {{
                margin-top: 2cm;
                page-break-inside: avoid;
                display: flex;
                flex-direction: column;
                align-items: center;
            }}
            .date {{
                margin-top: 0.5cm;
                font-style: italic;
            }}
            .official-stamp {{
                margin-top: 1cm;
                text-align: center;
                font-weight: bold;
                color: #1E3A8A;
                border: 2px solid #1E3A8A;
                padding: 0.5cm;
                border-radius: 5px;
                display: inline-block;
            }}
            .highlight {{
                background-color: #f0f7ff;
                padding: 0.5cm;
                border-right: 4px solid #1E3A8A;
                margin: 0.5cm 0;
                border-radius: 0 5px 5px 0;
            }}
            .scenario-box {{
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                padding: 1cm;
                margin: 0.5cm 0;
                border-radius: 5px;
            }}
            .laws-box {{
                background-color: #f0f7ff;
                border: 1px solid #cce5ff;
                padding: 1cm;
                margin: 0.5cm 0;
                border-radius: 5px;
            }}
            .implications-box {{
                background-color: #fff8f0;
                border: 1px solid #ffe0cc;
                padding: 1cm;
                margin: 0.5cm 0;
                border-radius: 5px;
            }}
            .penalties-box {{
                background-color: #fff0f0;
                border: 1px solid #ffcccc;
                padding: 1cm;
                margin: 0.5cm 0;
                border-radius: 5px;
            }}
            .procedures-box {{
                background-color: #f0fff0;
                border: 1px solid #ccffcc;
                padding: 1cm;
                margin: 0.5cm 0;
                border-radius: 5px;
            }}
            .conclusion-box {{
                background-color: #f0f0ff;
                border: 1px solid #ccccff;
                padding: 1cm;
                margin: 0.5cm 0;
                border-radius: 5px;
            }}
            .references-box {{
                background-color: #f9f9f9;
                border: 1px solid #ddd;
                padding: 1cm;
                margin: 0.5cm 0;
                border-radius: 5px;
                font-size: 10pt;
            }}
            strong {{
                color: #1E3A8A;
            }}
            p {{
                margin: 0.5cm 0;
            }}
            .watermark {{
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%) rotate(-45deg);
                font-size: 80pt;
                color: rgba(200, 200, 200, 0.1);
                z-index: -1;
                pointer-events: none;
            }}
            .logo {{
                text-align: center;
                margin-bottom: 0.5cm;
            }}
            .logo-text {{
                font-size: 18pt;
                font-weight: bold;
                color: #1E3A8A;
                border: 2px solid #1E3A8A;
                padding: 0.3cm;
                display: inline-block;
                border-radius: 5px;
            }}
        </style>
    </head>
    <body>
    <div class="watermark">سلطنة عمان</div>
    """
    
    # Add header with logo
    html += f"""
    <div class="header">
        <div class="logo">
            <div class="logo-text">⚖️ المساعد القانوني الذكي</div>
        </div>
        <div class="title">{content.get('title', 'تقرير تحليل قانوني')}</div>
        <div class="subtitle">{content.get('subtitle', '')}</div>
    </div>
    """
    
    # Add content with improved styling
    main_content = content.get('content', [])
    if main_content:
        html += "<div class='content'>"
        
        for i, paragraph in enumerate(main_content):
            # Determine which type of content this is based on the first few characters
            if paragraph.startswith("**السيناريو:**"):
                box_class = "scenario-box"
            elif paragraph.startswith("**القوانين والمواد"):
                box_class = "laws-box"
            elif paragraph.startswith("**التحليل القانوني"):
                box_class = "implications-box"
            elif paragraph.startswith("**العقوبات"):
                box_class = "penalties-box"
            elif paragraph.startswith("**الإجراءات"):
                box_class = "procedures-box"
            elif paragraph.startswith("**الخلاصة:**"):
                box_class = "conclusion-box"
            elif paragraph.startswith("**المراجع:**"):
                box_class = "references-box"
            elif paragraph.startswith("**عناصر القضية:**"):
                box_class = "scenario-box"
            else:
                box_class = ""
            
            # Convert markdown-style bold to HTML
            paragraph = paragraph.replace('**', '<strong>', 1)
            paragraph = paragraph.replace('**', '</strong>', 1)
            
            # Add section div with appropriate class
            html += f"<div class='section {box_class}'>"
            html += f"<p>{paragraph}</p>"
            html += "</div>"
        
        html += "</div>"
    
    # Add date and official stamp
    date_str = content.get('date', datetime.datetime.now().strftime("%Y-%m-%d"))
    html += f"""
    <div class="signature">
        <div class="date">تاريخ: {date_str}</div>
        <div class="official-stamp">المساعد القانوني الذكي لسلطنة عمان</div>
    </div>
    """
    
    # Add footer
    html += f"""
    <div class="footer">
        <p>هذا التقرير تم إنشاؤه بواسطة المساعد القانوني الذكي لسلطنة عمان</p>
        <p>يرجى ملاحظة أن هذا التحليل استشاري فقط وليس بديلاً عن الاستشارة القانونية المتخصصة</p>
    </div>
    """
    
    # Close HTML
    html += """
    </body>
    </html>
    """
    
    return html


# Initialize the template extension
add_case_report_template_to_document_generator()
