"""
Management command to verify all API configurations
"""
from django.core.management.base import BaseCommand
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Verify all API configurations and credentials'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔍 Checking API Configurations\n'))
        
        all_ok = True

        # Check WhatsApp configuration
        self.stdout.write('WhatsApp Business API:')
        if settings.WHATSAPP_ACCESS_TOKEN:
            self.stdout.write(self.style.SUCCESS('  ✅ Access Token: Configured'))
        else:
            self.stdout.write(self.style.ERROR('  ❌ Access Token: Missing'))
            all_ok = False

        if settings.WHATSAPP_PHONE_NUMBER_ID:
            self.stdout.write(self.style.SUCCESS('  ✅ Phone Number ID: Configured'))
        else:
            self.stdout.write(self.style.ERROR('  ❌ Phone Number ID: Missing'))
            all_ok = False

        if settings.WHATSAPP_VERIFY_TOKEN:
            self.stdout.write(self.style.SUCCESS('  ✅ Verify Token: Configured'))
        else:
            self.stdout.write(self.style.WARNING('  ⚠️  Verify Token: Using default'))

        # Check Gemini configuration
        self.stdout.write('\nGoogle Gemini API:')
        if settings.GEMINI_API_KEY:
            self.stdout.write(self.style.SUCCESS('  ✅ API Key: Configured'))
            
            # Test Gemini connection
            try:
                import google.generativeai as genai
                genai.configure(api_key=settings.GEMINI_API_KEY)
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content('Test')
                self.stdout.write(self.style.SUCCESS('  ✅ Connection: Successful'))
            except ImportError:
                self.stdout.write(self.style.ERROR('  ❌ Library: google-generativeai not installed'))
                all_ok = False
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ❌ Connection failed: {str(e)}'))
                all_ok = False
        else:
            self.stdout.write(self.style.ERROR('  ❌ API Key: Missing'))
            all_ok = False

        # Check Google Sheets configuration
        self.stdout.write('\nGoogle Sheets API:')
        if os.path.exists(settings.GOOGLE_SHEETS_CREDENTIALS_PATH):
            self.stdout.write(self.style.SUCCESS(f'  ✅ Credentials file: Found ({settings.GOOGLE_SHEETS_CREDENTIALS_PATH})'))
        else:
            self.stdout.write(self.style.ERROR(f'  ❌ Credentials file: Not found ({settings.GOOGLE_SHEETS_CREDENTIALS_PATH})'))
            all_ok = False

        if settings.GOOGLE_SHEET_ID:
            self.stdout.write(self.style.SUCCESS('  ✅ Sheet ID: Configured'))
        else:
            self.stdout.write(self.style.ERROR('  ❌ Sheet ID: Missing'))
            all_ok = False

        # Check required Python packages
        self.stdout.write('\nPython Packages:')
        packages = [
            ('gspread', 'Google Sheets'),
            ('oauth2client', 'Google OAuth'),
            ('google.generativeai', 'Gemini AI'),
            ('PyPDF2', 'PDF extraction'),
            ('requests', 'HTTP requests'),
        ]

        for package, description in packages:
            try:
                __import__(package)
                self.stdout.write(self.style.SUCCESS(f'  ✅ {description}: Installed'))
            except ImportError:
                self.stdout.write(self.style.ERROR(f'  ❌ {description}: Not installed'))
                all_ok = False

        # Summary
        self.stdout.write('\n' + '='*50)
        if all_ok:
            self.stdout.write(self.style.SUCCESS('\n✅ All configurations are valid!'))
            self.stdout.write('You can start using the application.\n')
        else:
            self.stdout.write(self.style.ERROR('\n❌ Some configurations are missing or invalid.'))
            self.stdout.write('Please check the errors above and update your .env file.\n')
