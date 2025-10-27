"""
Google Sheets Service
Handles data storage in Google Sheets
"""
import logging
from datetime import datetime
from django.conf import settings

logger = logging.getLogger(__name__)


class SheetsService:
    """Service for Google Sheets operations"""
    
    def __init__(self):
        self.credentials_path = settings.GOOGLE_SHEETS_CREDENTIALS_PATH
        self.sheet_id = settings.GOOGLE_SHEET_ID
        self.sheet = None
        self._initialize_sheet()
    
    def _initialize_sheet(self):
        """Initialize Google Sheets connection"""
        try:
            import gspread
            from oauth2client.service_account import ServiceAccountCredentials
            
            # Define the scope
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            
            # Add credentials
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                self.credentials_path, scope
            )
            
            # Authorize and open the sheet
            client = gspread.authorize(credentials)
            self.sheet = client.open_by_key(self.sheet_id).sheet1
            
            # Initialize headers if needed
            self._ensure_headers()
            
            logger.info('Google Sheets initialized successfully')
            
        except ImportError:
            logger.error('gspread or oauth2client not installed')
        except FileNotFoundError:
            logger.error(f'Credentials file not found: {self.credentials_path}')
        except Exception as e:
            logger.error(f'Error initializing Google Sheets: {str(e)}', exc_info=True)
    
    def _ensure_headers(self):
        """Ensure the sheet has proper headers"""
        try:
            if self.sheet:
                # Check if first row is empty
                first_row = self.sheet.row_values(1)
                
                if not first_row:
                    # Add headers
                    headers = [
                        'Name',
                        'Email',
                        'Phone',
                        'LinkedIn',
                        'Skills',
                        'WhatsApp Number',
                        'Timestamp'
                    ]
                    self.sheet.insert_row(headers, 1)
                    logger.info('Headers added to Google Sheet')
                    
        except Exception as e:
            logger.error(f'Error ensuring headers: {str(e)}', exc_info=True)
    
    def append_cv_data(self, cv_data):
        """
        Append CV data to Google Sheets
        
        Args:
            cv_data: Dictionary containing CV information
            
        Returns:
            bool: Success status
        """
        try:
            if not self.sheet:
                logger.error('Google Sheets not initialized')
                return False
            
            # Prepare row data
            row = [
                cv_data.get('name', ''),
                cv_data.get('email', ''),
                cv_data.get('phone', ''),
                cv_data.get('linkedin', ''),
                cv_data.get('skills', ''),
                cv_data.get('whatsapp_number', ''),
                datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
            ]
            
            # Append row
            self.sheet.append_row(row)
            
            logger.info(f'CV data appended to Google Sheets: {cv_data.get("name", "Unknown")}')
            return True
            
        except Exception as e:
            logger.error(f'Error appending to Google Sheets: {str(e)}', exc_info=True)
            return False
