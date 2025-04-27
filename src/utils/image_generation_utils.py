"""
Utility functions for image generation in the Legal AI Assistant.
"""

import io
import os
import datetime
from typing import Dict, Any, Optional, Tuple, List
from PIL import Image, ImageDraw, ImageFont, ImageColor
import numpy as np

class ImageGenerator:
    """Class for generating document-related images."""
    
    def __init__(self, templates_dir: str = None):
        """
        Initialize the image generator.
        
        Args:
            templates_dir: Directory containing image templates
        """
        self.templates_dir = templates_dir or os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "templates")
        os.makedirs(self.templates_dir, exist_ok=True)
        
        # Try to load fonts
        self.fonts = self._load_fonts()
    
    def generate_certificate(self, content: Dict[str, Any], 
                            width: int = 1000, height: int = 1400) -> bytes:
        """
        Generate a certificate image.
        
        Args:
            content: Dictionary containing certificate content
            width: Image width
            height: Image height
            
        Returns:
            Certificate image as bytes
        """
        # Create a new image with white background
        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image)
        
        # Draw decorative border
        self._draw_decorative_border(draw, width, height)
        
        # Draw header
        self._draw_certificate_header(draw, width, content)
        
        # Draw content
        self._draw_certificate_content(draw, width, height, content)
        
        # Draw footer with seal
        self._draw_certificate_footer(draw, width, height, content)
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()
    
    def generate_contract_cover(self, content: Dict[str, Any],
                               width: int = 1000, height: int = 1400) -> bytes:
        """
        Generate a contract cover image.
        
        Args:
            content: Dictionary containing contract content
            width: Image width
            height: Image height
            
        Returns:
            Contract cover image as bytes
        """
        # Create a new image with gradient background
        image = self._create_gradient_background(width, height, 
                                               start_color='#F0F8FF', 
                                               end_color='#E6F0FF')
        draw = ImageDraw.Draw(image)
        
        # Draw decorative elements
        self._draw_decorative_elements(draw, width, height)
        
        # Draw title
        title = content.get('title', 'عقد قانوني')
        self._draw_text_with_shadow(draw, width//2, height//4, title, 
                                  self.fonts.get('title', self.fonts['default']),
                                  fill='#1E3A8A')
        
        # Draw contract type
        contract_type = content.get('contract_type', 'عقد')
        if contract_type == 'employment':
            contract_type = 'عقد عمل'
        self._draw_text_with_shadow(draw, width//2, height//4 + 80, contract_type, 
                                  self.fonts.get('subtitle', self.fonts['default']),
                                  fill='#2E4A9A')
        
        # Draw parties
        first_party = content.get('first_party', 'الطرف الأول')
        second_party = content.get('second_party', 'الطرف الثاني')
        
        y_pos = height//2
        self._draw_text_with_shadow(draw, width//2, y_pos, "بين", 
                                  self.fonts.get('body', self.fonts['default']),
                                  fill='#000000')
        
        y_pos += 60
        self._draw_text_with_shadow(draw, width//2, y_pos, first_party, 
                                  self.fonts.get('body', self.fonts['default']),
                                  fill='#000000')
        
        y_pos += 40
        self._draw_text_with_shadow(draw, width//2, y_pos, "و", 
                                  self.fonts.get('body', self.fonts['default']),
                                  fill='#000000')
        
        y_pos += 40
        self._draw_text_with_shadow(draw, width//2, y_pos, second_party, 
                                  self.fonts.get('body', self.fonts['default']),
                                  fill='#000000')
        
        # Draw date
        date_str = content.get('date', datetime.datetime.now().strftime("%Y-%m-%d"))
        self._draw_text_with_shadow(draw, width//2, height - 200, f"تاريخ: {date_str}", 
                                  self.fonts.get('body', self.fonts['default']),
                                  fill='#000000')
        
        # Draw official seal
        self._draw_official_seal(draw, width//2, height - 100, 80)
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()
    
    def generate_authorization_image(self, content: Dict[str, Any],
                                    width: int = 1000, height: int = 1400) -> bytes:
        """
        Generate an authorization document image.
        
        Args:
            content: Dictionary containing authorization content
            width: Image width
            height: Image height
            
        Returns:
            Authorization image as bytes
        """
        # Create a new image with light background
        image = self._create_gradient_background(width, height, 
                                               start_color='#FFF8E1', 
                                               end_color='#FFECB3')
        draw = ImageDraw.Draw(image)
        
        # Draw border
        self._draw_simple_border(draw, width, height)
        
        # Draw title
        title = content.get('title', 'تفويض')
        self._draw_text_with_shadow(draw, width//2, height//6, title, 
                                  self.fonts.get('title', self.fonts['default']),
                                  fill='#5D4037')
        
        # Draw content
        authorizer = content.get('authorizer', 'المفوض')
        authorized = content.get('authorized', 'المفوض إليه')
        purpose = content.get('purpose', 'الغرض من التفويض')
        
        y_pos = height//3
        self._draw_text_with_shadow(draw, width//2, y_pos, f"من: {authorizer}", 
                                  self.fonts.get('body', self.fonts['default']),
                                  fill='#000000')
        
        y_pos += 60
        self._draw_text_with_shadow(draw, width//2, y_pos, f"إلى: {authorized}", 
                                  self.fonts.get('body', self.fonts['default']),
                                  fill='#000000')
        
        y_pos += 60
        self._draw_text_with_shadow(draw, width//2, y_pos, f"الغرض: {purpose}", 
                                  self.fonts.get('body', self.fonts['default']),
                                  fill='#000000')
        
        # Draw date
        date_str = content.get('date', datetime.datetime.now().strftime("%Y-%m-%d"))
        self._draw_text_with_shadow(draw, width//2, height - 200, f"تاريخ: {date_str}", 
                                  self.fonts.get('body', self.fonts['default']),
                                  fill='#000000')
        
        # Draw signature line
        self._draw_signature_line(draw, width//2, height - 120, 200)
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()
    
    def _load_fonts(self) -> Dict[str, Any]:
        """Load fonts for image generation."""
        fonts = {'default': ImageFont.load_default()}
        
        try:
            # Try to load common fonts
            fonts['title'] = ImageFont.truetype("Arial", 48)
            fonts['subtitle'] = ImageFont.truetype("Arial", 36)
            fonts['header'] = ImageFont.truetype("Arial", 24)
            fonts['body'] = ImageFont.truetype("Arial", 18)
            fonts['small'] = ImageFont.truetype("Arial", 14)
        except IOError:
            # Fallback to default font if specific fonts are not available
            fonts['title'] = ImageFont.load_default()
            fonts['subtitle'] = ImageFont.load_default()
            fonts['header'] = ImageFont.load_default()
            fonts['body'] = ImageFont.load_default()
            fonts['small'] = ImageFont.load_default()
        
        return fonts
    
    def _create_gradient_background(self, width: int, height: int, 
                                   start_color: str, end_color: str) -> Image.Image:
        """Create an image with a gradient background."""
        # Convert hex colors to RGB
        start_rgb = ImageColor.getrgb(start_color)
        end_rgb = ImageColor.getrgb(end_color)
        
        # Create gradient array
        arr = np.zeros((height, width, 3), dtype=np.uint8)
        for y in range(height):
            r = start_rgb[0] + (end_rgb[0] - start_rgb[0]) * y // height
            g = start_rgb[1] + (end_rgb[1] - start_rgb[1]) * y // height
            b = start_rgb[2] + (end_rgb[2] - start_rgb[2]) * y // height
            arr[y, :] = [r, g, b]
        
        # Convert array to image
        return Image.fromarray(arr)
    
    def _draw_decorative_border(self, draw: ImageDraw, width: int, height: int):
        """Draw a decorative border on the image."""
        # Outer border
        draw.rectangle([(20, 20), (width-20, height-20)], outline='#1E3A8A', width=3)
        
        # Inner border
        draw.rectangle([(40, 40), (width-40, height-40)], outline='#1E3A8A', width=1)
        
        # Corner decorations
        corner_size = 30
        
        # Top-left corner
        draw.line([(20, 60), (60, 20)], fill='#1E3A8A', width=2)
        draw.line([(20, 80), (80, 20)], fill='#1E3A8A', width=2)
        
        # Top-right corner
        draw.line([(width-20, 60), (width-60, 20)], fill='#1E3A8A', width=2)
        draw.line([(width-20, 80), (width-80, 20)], fill='#1E3A8A', width=2)
        
        # Bottom-left corner
        draw.line([(20, height-60), (60, height-20)], fill='#1E3A8A', width=2)
        draw.line([(20, height-80), (80, height-20)], fill='#1E3A8A', width=2)
        
        # Bottom-right corner
        draw.line([(width-20, height-60), (width-60, height-20)], fill='#1E3A8A', width=2)
        draw.line([(width-20, height-80), (width-80, height-20)], fill='#1E3A8A', width=2)
    
    def _draw_simple_border(self, draw: ImageDraw, width: int, height: int):
        """Draw a simple border on the image."""
        # Outer border
        draw.rectangle([(20, 20), (width-20, height-20)], outline='#5D4037', width=3)
        
        # Inner border
        draw.rectangle([(40, 40), (width-40, height-40)], outline='#8D6E63', width=1)
    
    def _draw_decorative_elements(self, draw: ImageDraw, width: int, height: int):
        """Draw decorative elements on the image."""
        # Header decoration
        draw.rectangle([(40, 40), (width-40, 120)], fill='#1E3A8A', outline=None)
        draw.rectangle([(60, 120), (width-60, 123)], fill='#FFC107', outline=None)
        
        # Footer decoration
        draw.rectangle([(40, height-120), (width-40, height-40)], fill='#1E3A8A', outline=None)
        draw.rectangle([(60, height-123), (width-60, height-120)], fill='#FFC107', outline=None)
    
    def _draw_certificate_header(self, draw: ImageDraw, width: int, content: Dict[str, Any]):
        """Draw the certificate header."""
        # Title
        title = content.get('title', 'شهادة')
        self._draw_text_with_shadow(draw, width//2, 100, title, 
                                  self.fonts.get('title', self.fonts['default']),
                                  fill='#1E3A8A')
        
        # Subtitle
        subtitle = content.get('subtitle', '')
        if subtitle:
            self._draw_text_with_shadow(draw, width//2, 160, subtitle, 
                                      self.fonts.get('subtitle', self.fonts['default']),
                                      fill='#1E3A8A')
    
    def _draw_certificate_content(self, draw: ImageDraw, width: int, height: int, content: Dict[str, Any]):
        """Draw the certificate content."""
        # Main content
        y_pos = height // 3
        
        # Certificate text
        certificate_text = content.get('certificate_text', 'هذه الشهادة تمنح إلى')
        self._draw_text_with_shadow(draw, width//2, y_pos, certificate_text, 
                                  self.fonts.get('body', self.fonts['default']),
                                  fill='#000000')
        
        # User name
        y_pos += 80
        user_name = content.get('user_name', content.get('second_party', 'المستخدم'))
        self._draw_text_with_shadow(draw, width//2, y_pos, user_name, 
                                  self.fonts.get('subtitle', self.fonts['default']),
                                  fill='#1E3A8A')
        
        # Additional content
        y_pos += 80
        additional_text = content.get('additional_text', '')
        if additional_text:
            self._draw_text_with_shadow(draw, width//2, y_pos, additional_text, 
                                      self.fonts.get('body', self.fonts['default']),
                                      fill='#000000')
    
    def _draw_certificate_footer(self, draw: ImageDraw, width: int, height: int, content: Dict[str, Any]):
        """Draw the certificate footer."""
        # Date
        date_str = content.get('date', datetime.datetime.now().strftime("%Y-%m-%d"))
        self._draw_text_with_shadow(draw, width//2, height - 200, f"تاريخ: {date_str}", 
                                  self.fonts.get('body', self.fonts['default']),
                                  fill='#000000')
        
        # Official seal
        self._draw_official_seal(draw, width//2, height - 100, 80)
    
    def _draw_text_with_shadow(self, draw: ImageDraw, x: int, y: int, text: str, font, fill: str = 'black'):
        """Draw text with a subtle shadow effect."""
        # Draw shadow
        draw.text((x+2, y+2), text, font=font, fill='#CCCCCC', anchor='mm')
        
        # Draw text
        draw.text((x, y), text, font=font, fill=fill, anchor='mm')
    
    def _draw_official_seal(self, draw: ImageDraw, x: int, y: int, size: int):
        """Draw an official-looking seal on the image."""
        # Outer circle
        draw.ellipse([(x-size, y-size), (x+size, y+size)], outline='#1E3A8A', width=3)
        
        # Inner circle
        inner_size = size * 0.8
        draw.ellipse([(x-inner_size, y-inner_size), (x+inner_size, y+inner_size)], outline='#1E3A8A', width=2)
        
        # Center text
        draw.text((x, y-10), "سلطنة عمان", fill='#1E3A8A', font=self.fonts.get('small', self.fonts['default']), anchor='mm')
        draw.text((x, y+10), "وثيقة رسمية", fill='#1E3A8A', font=self.fonts.get('small', self.fonts['default']), anchor='mm')
    
    def _draw_signature_line(self, draw: ImageDraw, x: int, y: int, width: int):
        """Draw a signature line."""
        half_width = width // 2
        draw.line([(x-half_width, y), (x+half_width, y)], fill='#000000', width=1)
        draw.text((x, y-20), "التوقيع", fill='#000000', font=self.fonts.get('small', self.fonts['default']), anchor='mm')
