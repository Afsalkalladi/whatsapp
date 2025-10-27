"""
Gemini Service
Handles CV data extraction using Google's Gemini API
"""
import logging
import json
from django.conf import settings

logger = logging.getLogger(__name__)


class GeminiService:
    """Service for extracting structured CV data using Gemini AI"""
    
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        
    def extract_cv_data(self, cv_text):
        """
        Extract structured data from CV text using Gemini API
        
        Args:
            cv_text: Raw CV text
            
        Returns:
            dict: Structured CV data with keys: name, email, phone, linkedin, skills
        """
        try:
            import google.generativeai as genai
            
            # Configure Gemini
            genai.configure(api_key=self.api_key)
            
            # Use gemini-2.5-flash (faster and higher free tier quota)
            # Flash models have 1500 requests/day vs Pro's 50 requests/day
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
                logger.info('Using model: gemini-2.5-flash')
            except Exception as model_error:
                logger.error(f'Error creating model: {model_error}')
                return None
            
            # Create prompt for structured extraction
            prompt = f"""
You are a CV/Resume parser. Extract the following information from the CV text below and return it in valid JSON format.

Required fields:
- name (string): Full name of the candidate
- email (string): Email address
- phone (string): Phone number

Optional fields:
- linkedin (string): LinkedIn profile URL
- skills (string): Comma-separated list of skills

Important:
- Return ONLY valid JSON, no additional text
- If a field is not found, use null
- For phone, include country code if present
- For skills, extract up to 10 most relevant skills

CV Text:
{cv_text}

Return JSON in this exact format:
{{
  "name": "...",
  "email": "...",
  "phone": "...",
  "linkedin": "...",
  "skills": "..."
}}
"""
            
            # Generate response
            response = model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean response (remove markdown code blocks if present)
            if response_text.startswith('```'):
                response_text = response_text.split('```')[1]
                if response_text.startswith('json'):
                    response_text = response_text[4:]
                response_text = response_text.strip()
            
            # Parse JSON
            cv_data = json.loads(response_text)
            
            logger.info(f'Extracted CV data: {cv_data}')
            return cv_data
            
        except ImportError:
            logger.error('google-generativeai not installed. Install with: pip install google-generativeai')
            return None
        except json.JSONDecodeError as e:
            logger.error(f'Failed to parse Gemini response as JSON: {str(e)}')
            logger.error(f'Response text: {response_text}')
            return None
        except Exception as e:
            logger.error(f'Error extracting CV data with Gemini: {str(e)}', exc_info=True)
            return None
