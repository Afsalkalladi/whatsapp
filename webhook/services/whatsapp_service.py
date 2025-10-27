"""
WhatsApp Service
Handles communication with WhatsApp Business API
"""
import os
import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class WhatsAppService:
    """Service for WhatsApp Business API operations"""
    
    def __init__(self):
        self.access_token = settings.WHATSAPP_ACCESS_TOKEN
        self.phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
        self.base_url = f"https://graph.facebook.com/v18.0/{self.phone_number_id}"
        
    def download_media(self, media_id):
        """
        Download media file from WhatsApp
        
        Args:
            media_id: WhatsApp media ID
            
        Returns:
            str: Path to downloaded file or None
        """
        try:
            # Get media URL
            url = f"https://graph.facebook.com/v18.0/{media_id}"
            headers = {
                'Authorization': f'Bearer {self.access_token}'
            }
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            media_data = response.json()
            media_url = media_data.get('url')
            
            if not media_url:
                logger.error('No media URL in response')
                return None
            
            # Download the file
            media_response = requests.get(media_url, headers=headers)
            media_response.raise_for_status()
            
            # Save to temp file
            os.makedirs('media/temp', exist_ok=True)
            file_path = f'media/temp/{media_id}.pdf'
            
            with open(file_path, 'wb') as f:
                f.write(media_response.content)
            
            logger.info(f'Downloaded media to {file_path}')
            return file_path
            
        except Exception as e:
            logger.error(f'Error downloading media: {str(e)}', exc_info=True)
            return None
    
    def send_message(self, to_number, message):
        """
        Send a text message via WhatsApp
        
        Args:
            to_number: Recipient phone number
            message: Message text
            
        Returns:
            bool: Success status
        """
        try:
            url = f"{self.base_url}/messages"
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'messaging_product': 'whatsapp',
                'to': to_number,
                'type': 'text',
                'text': {
                    'body': message
                }
            }
            
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            
            logger.info(f'Message sent to {to_number}')
            return True
            
        except Exception as e:
            logger.error(f'Error sending message: {str(e)}', exc_info=True)
            return False
