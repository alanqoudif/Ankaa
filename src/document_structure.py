"""
Document structure analyzer for legal documents.
Identifies sections, articles, and other structural elements in legal texts.
"""

import re
from typing import List, Dict, Any, Optional, Tuple

class DocumentStructureAnalyzer:
    """Analyzes the structure of legal documents to identify sections and articles."""
    
    def __init__(self):
        """Initialize the document structure analyzer."""
        # Regex patterns for identifying articles and sections in both English and Arabic
        self.article_patterns = [
            # English patterns
            r'Article\s+(\d+)[:\.\s]',
            r'Section\s+(\d+)[:\.\s]',
            # Arabic patterns
            r'المادة\s+(\d+)[:\.\s]',
            r'مادة\s+(\d+)[:\.\s]',
            r'الفصل\s+(\d+)[:\.\s]',
            r'القسم\s+(\d+)[:\.\s]'
        ]
        
        # Patterns for section titles
        self.section_title_patterns = [
            # English patterns
            r'Chapter\s+(\d+)[:\.\s]',
            r'Part\s+(\d+)[:\.\s]',
            r'Title\s+(\d+)[:\.\s]',
            # Arabic patterns
            r'الباب\s+(\d+)[:\.\s]',
            r'الفصل\s+(\d+)[:\.\s]',
            r'الجزء\s+(\d+)[:\.\s]',
            r'العنوان\s+(\d+)[:\.\s]'
        ]
    
    def extract_articles(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract articles from the text.
        
        Args:
            text: The text to analyze
            
        Returns:
            List of dictionaries containing article information
        """
        articles = []
        
        # Find all article matches
        all_matches = []
        for pattern in self.article_patterns:
            matches = list(re.finditer(pattern, text))
            for match in matches:
                all_matches.append((match.start(), match.group(), match.group(1)))
        
        # Sort matches by position in text
        all_matches.sort(key=lambda x: x[0])
        
        # Extract article content
        for i, (pos, full_match, article_num) in enumerate(all_matches):
            # Determine end position (start of next article or end of text)
            end_pos = len(text)
            if i < len(all_matches) - 1:
                end_pos = all_matches[i+1][0]
            
            # Extract article content
            content = text[pos:end_pos].strip()
            
            # Create article object
            article = {
                "id": article_num,
                "type": "article",
                "full_match": full_match,
                "content": content,
                "position": pos
            }
            
            articles.append(article)
        
        return articles
    
    def extract_sections(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract sections from the text.
        
        Args:
            text: The text to analyze
            
        Returns:
            List of dictionaries containing section information
        """
        sections = []
        
        # Find all section matches
        all_matches = []
        for pattern in self.section_title_patterns:
            matches = list(re.finditer(pattern, text))
            for match in matches:
                all_matches.append((match.start(), match.group(), match.group(1)))
        
        # Sort matches by position in text
        all_matches.sort(key=lambda x: x[0])
        
        # Extract section content
        for i, (pos, full_match, section_num) in enumerate(all_matches):
            # Determine end position (start of next section or end of text)
            end_pos = len(text)
            if i < len(all_matches) - 1:
                end_pos = all_matches[i+1][0]
            
            # Extract section content
            content = text[pos:end_pos].strip()
            
            # Create section object
            section = {
                "id": section_num,
                "type": "section",
                "full_match": full_match,
                "content": content,
                "position": pos
            }
            
            sections.append(section)
        
        return sections
    
    def find_article_by_number(self, text: str, article_number: str) -> Optional[Dict[str, Any]]:
        """
        Find a specific article by its number.
        
        Args:
            text: The text to search in
            article_number: The article number to find
            
        Returns:
            Dictionary with article information or None if not found
        """
        articles = self.extract_articles(text)
        
        # Find the article with the matching number
        for article in articles:
            if article["id"] == article_number:
                return article
        
        return None
    
    def find_section_by_number(self, text: str, section_number: str) -> Optional[Dict[str, Any]]:
        """
        Find a specific section by its number.
        
        Args:
            text: The text to search in
            section_number: The section number to find
            
        Returns:
            Dictionary with section information or None if not found
        """
        sections = self.extract_sections(text)
        
        # Find the section with the matching number
        for section in sections:
            if section["id"] == section_number:
                return section
        
        return None
    
    def analyze_document_structure(self, text: str) -> Dict[str, Any]:
        """
        Analyze the structure of a document.
        
        Args:
            text: The text to analyze
            
        Returns:
            Dictionary with document structure information
        """
        articles = self.extract_articles(text)
        sections = self.extract_sections(text)
        
        return {
            "articles": articles,
            "sections": sections,
            "article_count": len(articles),
            "section_count": len(sections)
        }
    
    def extract_article_title(self, article_content: str) -> str:
        """
        Extract the title of an article.
        
        Args:
            article_content: The content of the article
            
        Returns:
            The title of the article
        """
        # Try to find a title line after the article declaration
        lines = article_content.split('\n')
        if len(lines) > 1:
            # Skip the first line (which contains the article number)
            for line in lines[1:3]:  # Check the next couple of lines for a title
                line = line.strip()
                if line and not line.startswith('(') and not re.match(r'^\d+\.', line):
                    return line
        
        # If no title found, return the first line
        return lines[0] if lines else article_content[:50] + "..."
