"""
PDF Service
Handles PDF text extraction using Adobe PDF Services API
"""
import os
import logging
import requests
import json
from django.conf import settings

logger = logging.getLogger(__name__)


class PDFService:
    """Service for PDF text extraction"""
    
    def __init__(self):
        self.client_id = settings.ADOBE_CLIENT_ID
        self.client_secret = settings.ADOBE_CLIENT_SECRET
        
    def extract_text(self, pdf_path):
        """
        Extract text from PDF file using Adobe PDF Services API
        
        For MVP: Using a simpler approach with PyPDF2 as fallback
        Adobe PDF Services requires more complex setup
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            str: Extracted text
        """
        try:
            # Try Adobe PDF Services if credentials are configured
            if self.client_id and self.client_secret:
                return self._extract_with_adobe(pdf_path)
            else:
                # Fallback to PyPDF2
                return self._extract_with_pypdf2(pdf_path)
                
        except Exception as e:
            logger.error(f'Error extracting PDF text: {str(e)}', exc_info=True)
            return None
    
    def _extract_with_adobe(self, pdf_path):
        """
        Extract text using Adobe PDF Services API
        
        NOTE: This is a simplified implementation
        For production, use the official Adobe PDF Services SDK
        """
        try:
            # Get access token
            token_url = 'https://ims-na1.adobelogin.com/ims/token/v3'
            token_data = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'grant_type': 'client_credentials',
                'scope': 'openid,AdobeID,read_organizations'
            }
            
            token_response = requests.post(token_url, data=token_data)
            token_response.raise_for_status()
            access_token = token_response.json().get('access_token')
            
            # Upload PDF
            # Note: Full implementation requires Adobe PDF Extract API
            # This is a placeholder for the complete flow
            
            logger.warning('Adobe PDF Services integration requires full SDK setup')
            return self._extract_with_pypdf2(pdf_path)
            
        except Exception as e:
            logger.error(f'Adobe API error: {str(e)}', exc_info=True)
            return self._extract_with_pypdf2(pdf_path)
    
    def _extract_with_pypdf2(self, pdf_path):
        """
        Fallback: Extract text using PyPDF2
        """
        try:
            import PyPDF2
            
            text = ''
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            
            logger.info(f'Extracted {len(text)} characters using PyPDF2')
            return text.strip()
            
        except ImportError:
            logger.error('PyPDF2 not installed. Install with: pip install PyPDF2')
            return None
        except Exception as e:
            logger.error(f'PyPDF2 extraction error: {str(e)}', exc_info=True)
            return None
