"""
Utility functions for handling Arabic text in the Legal AI Assistant.
"""

import re
from typing import List, Dict, Any

def normalize_arabic_text(text: str) -> str:
    """
    Normalize Arabic text by removing diacritics, normalizing characters, etc.
    
    Args:
        text: Arabic text to normalize
        
    Returns:
        Normalized Arabic text
    """
    if not text:
        return ""
    
    # Remove diacritics (tashkeel)
    text = re.sub(r'[\u064B-\u065F\u0670]', '', text)
    
    # Normalize alef forms
    text = re.sub(r'[إأآا]', 'ا', text)
    
    # Normalize yaa and alef maksura
    text = re.sub(r'[يى]', 'ي', text)
    
    # Normalize taa marbouta and haa
    text = re.sub(r'[ةه]', 'ه', text)
    
    # Normalize hamza forms
    text = re.sub(r'[ؤئ]', 'ء', text)
    
    return text

def detect_language(text: str) -> str:
    """
    Detect whether the text is primarily in Arabic or English.
    
    Args:
        text: Text to analyze
        
    Returns:
        'ar' for Arabic, 'en' for English, 'mixed' for mixed content
    """
    if not text:
        return "unknown"
    
    # Count Arabic and English characters
    arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]+')
    english_pattern = re.compile(r'[a-zA-Z]+')
    
    arabic_matches = arabic_pattern.findall(text)
    english_matches = english_pattern.findall(text)
    
    arabic_char_count = sum(len(match) for match in arabic_matches)
    english_char_count = sum(len(match) for match in english_matches)
    
    # Determine dominant language
    if arabic_char_count > english_char_count * 2:
        return "ar"
    elif english_char_count > arabic_char_count * 2:
        return "en"
    else:
        return "mixed"

def get_arabic_stopwords() -> List[str]:
    """
    Get a list of common Arabic stopwords.
    
    Returns:
        List of Arabic stopwords
    """
    return [
        "من", "إلى", "عن", "على", "في", "مع", "هذا", "هذه", "ذلك", "تلك",
        "هو", "هي", "هم", "هن", "انت", "انتم", "انتن", "انا", "نحن",
        "كان", "كانت", "كانوا", "يكون", "تكون", "اكون", "نكون",
        "ما", "لا", "لم", "لن", "ان", "اذا", "لو", "لكن", "و", "ف", "ثم", "او", "ام",
        "حتى", "الى", "الذي", "التي", "الذين", "اللذين", "اللتين", "اللاتي",
        "كل", "بعض", "غير", "كثير", "قليل", "جدا"
    ]


if __name__ == "__main__":
    # Example usage
    text = "هذا نص عربي مع بعض الكلمات الإنجليزية English words"
    normalized = normalize_arabic_text(text)
    language = detect_language(text)
    
    print(f"Original: {text}")
    print(f"Normalized: {normalized}")
    print(f"Detected language: {language}")
    
    stopwords = get_arabic_stopwords()
    print(f"Arabic stopwords (first 10): {stopwords[:10]}")
