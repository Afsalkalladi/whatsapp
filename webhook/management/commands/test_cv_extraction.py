"""
Management command to test CV extraction without WhatsApp
"""
from django.core.management.base import BaseCommand
from webhook.services.gemini_service import GeminiService
from webhook.services.sheets_service import SheetsService


class Command(BaseCommand):
    help = 'Test CV extraction from text file'

    def add_arguments(self, parser):
        parser.add_argument(
            'cv_file',
            type=str,
            help='Path to CV text file'
        )
        parser.add_argument(
            '--no-save',
            action='store_true',
            help='Don\'t save to Google Sheets'
        )

    def handle(self, *args, **options):
        cv_file = options['cv_file']
        no_save = options['no_save']

        self.stdout.write(self.style.SUCCESS(f'Reading CV from: {cv_file}'))

        try:
            # Read CV text
            with open(cv_file, 'r') as f:
                cv_text = f.read()

            self.stdout.write(f'CV text length: {len(cv_text)} characters\n')

            # Extract CV data
            self.stdout.write('Extracting CV data with Gemini...')
            gemini_service = GeminiService()
            cv_data = gemini_service.extract_cv_data(cv_text)

            if cv_data:
                self.stdout.write(self.style.SUCCESS('\n✅ Extraction successful!'))
                self.stdout.write('\nExtracted data:')
                self.stdout.write(f"  Name: {cv_data.get('name', 'N/A')}")
                self.stdout.write(f"  Email: {cv_data.get('email', 'N/A')}")
                self.stdout.write(f"  Phone: {cv_data.get('phone', 'N/A')}")
                self.stdout.write(f"  LinkedIn: {cv_data.get('linkedin', 'N/A')}")
                self.stdout.write(f"  Skills: {cv_data.get('skills', 'N/A')}")

                # Save to Google Sheets
                if not no_save:
                    self.stdout.write('\nSaving to Google Sheets...')
                    cv_data['whatsapp_number'] = 'TEST'
                    
                    sheets_service = SheetsService()
                    if sheets_service.append_cv_data(cv_data):
                        self.stdout.write(self.style.SUCCESS('✅ Saved to Google Sheets!'))
                    else:
                        self.stdout.write(self.style.ERROR('❌ Failed to save to Google Sheets'))
                else:
                    self.stdout.write(self.style.WARNING('\nSkipping Google Sheets save (--no-save flag)'))

            else:
                self.stdout.write(self.style.ERROR('❌ Extraction failed'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {cv_file}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
