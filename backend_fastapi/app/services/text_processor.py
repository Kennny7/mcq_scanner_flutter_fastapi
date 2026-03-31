import requests
import base64
import re
from app.core.logger import app_logger
from app.core.config import settings
from typing import List, Tuple, Dict, Optional

class TextProcessor:
    def __init__(self):
        self.mcq_pattern = r'([A-D])[\.\s\)]+\s*(.+?)(?=\s*(?:[A-D][\.\s\)]|$))'
        self.api_key = settings.OCR_SPACE_API_KEY
        self.api_url = "https://api.ocr.space/parse/image"

    def extract_text(self, image_bytes: bytes) -> tuple[str, float]:
        """Extract text from image bytes using OCR.Space API"""
        try:
            encoded_image = base64.b64encode(image_bytes).decode()

            payload = {
                'apikey': self.api_key,
                'base64Image': f"data:image/jpeg;base64,{encoded_image}",
                'language': 'eng',
                'isOverlayRequired': False,
                'OCREngine': 2
            }

            response = requests.post(self.api_url, data=payload, timeout=30)
            result = response.json()

            if result.get('IsErroredOnProcessing'):
                error_msg = result.get('ErrorMessage', 'Unknown OCR error')
                app_logger.error(f"OCR API error: {error_msg}")
                return "", 0.0

            parsed_results = result.get('ParsedResults', [])
            if parsed_results:
                text = parsed_results[0].get('ParsedText', '')
                confidence = float(parsed_results[0].get('TextOverlay', {}).get('MedianConfidence', 50))
                app_logger.info(f"OCR extracted text with confidence: {confidence}")
                return text, confidence / 100.0

            return "", 0.0

        except Exception as e:
            app_logger.error(f"OCR extraction error: {str(e)}")
            return "", 0.0

    def parse_mcq(self, text: str) -> Tuple[str, Dict[str, str]]:
        """Parse MCQ question and options, returning question and dict with keys A, B, C, D."""
        text = self.clean_text(text)
        lines = text.split('\n')
        
        question_lines = []
        options = []  # will store tuples (detected_label_if_any, text)
        current_option = None
        current_text = []
        
        # Patterns for option markers
        letter_pattern = re.compile(r'^([A-D])[\.\)]\s+(.*)', re.IGNORECASE)
        # Include slash as a possible bullet (OCR sometimes converts checkboxes to '/')
        bullet_pattern = re.compile(r'^[•\-\*/]\s+(.*)')
        number_pattern = re.compile(r'^(\d+)[\.\)]\s+(.*)')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check for lettered option
            match = letter_pattern.match(line)
            if match:
                if current_option is not None or current_text:
                    options.append((current_option, ' '.join(current_text).strip()))
                current_option = match.group(1).upper()
                current_text = [match.group(2).strip()]
                continue
            
            # Check for bullet/dash/asterisk/slash option
            match = bullet_pattern.match(line)
            if match:
                # Finalize any pending option
                if current_option is not None or current_text:
                    options.append((current_option, ' '.join(current_text).strip()))
                
                rest = match.group(1).strip()
                
                # If the line contains multiple option separators, split it
                if re.search(r'[•/]', rest):
                    parts = re.split(r'[•/]', rest)
                    for part in parts:
                        part = part.strip()
                        if part:
                            options.append((None, part))
                    # No pending option after splitting
                    current_option = None
                    current_text = []
                else:
                    # Single bullet option
                    current_option = None
                    current_text = [rest]
                continue
            
            # Check for numbered option
            match = number_pattern.match(line)
            if match:
                if current_option is not None or current_text:
                    options.append((current_option, ' '.join(current_text).strip()))
                current_option = None
                current_text = [match.group(2).strip()]
                continue
            
            # If we are inside an option, append to it
            if current_option is not None or current_text:
                current_text.append(line)
            else:
                # Not in an option → part of the question
                question_lines.append(line)
        
        # Don't forget the last option
        if current_text:
            options.append((current_option, ' '.join(current_text).strip()))
        
        # Build question
        question = ' '.join(question_lines).strip()
        question = self.clean_question(question)
        
        # Assign sequential letters A, B, C, ... to options in order
        option_dict = {}
        for i, (_, text) in enumerate(options):
            letter = chr(ord('A') + i)
            option_dict[letter] = text
        
        app_logger.info(f"Extracted question: '{question}'")
        app_logger.info(f"Extracted options: {option_dict}")
        
        return question, option_dict

    def clean_question(self, question: str) -> str:
        patterns = [
            r'^\s*\d+[\.\)]\s*',
            r'^\s*Title\s*',
            r'^\s*Question\s*\d*\s*',
            r'^\s*MCQ\s*\d*\s*',
            r'^\s*[Qq]\s*\d*[\.\)\:\-]\s*'
        ]
        for pattern in patterns:
            cleaned = re.sub(pattern, '', question, flags=re.IGNORECASE)
            if cleaned.strip() and cleaned != question:
                question = cleaned
        return question.strip()

    def clean_text(self, text: str) -> str:
        text = re.sub(r'[ \t]+', ' ', text)
        text = text.replace('|', 'I').replace('0', 'O')
        return text.strip()

    def is_valid_question(self, question: str, options: dict) -> bool:
        meaningful_question = len(question) > 20 or ('?' in question and len(question) > 10)
        valid_options = len(options) >= 2
        return meaningful_question and valid_options