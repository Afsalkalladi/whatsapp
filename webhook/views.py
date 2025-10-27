"""
WhatsApp Webhook Views
Handles incoming messages and files from WhatsApp Business API
"""
import json
import logging
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .services.whatsapp_service import WhatsAppService
from .services.pdf_service import PDFService
from .services.gemini_service import GeminiService
from .services.sheets_service import SheetsService

logger = logging.getLogger(__name__)

whatsapp_service = WhatsAppService()
pdf_service = PDFService()
gemini_service = GeminiService()
sheets_service = SheetsService()


def health_check(request):
    """Simple health check endpoint for Render"""
    return JsonResponse({'status': 'ok'})


@csrf_exempt
def whatsapp_webhook(request):
    """
    Handle WhatsApp webhook verification and incoming messages
    """
    if request.method == 'GET':
        # Webhook verification
        return verify_webhook(request)
    elif request.method == 'POST':
        # Handle incoming messages
        return handle_incoming_message(request)
    
    return HttpResponse(status=405)


def verify_webhook(request):
    """
    Verify webhook with WhatsApp Business API
    """
    mode = request.GET.get('hub.mode')
    token = request.GET.get('hub.verify_token')
    challenge = request.GET.get('hub.challenge')
    
    if mode == 'subscribe' and token == settings.WHATSAPP_VERIFY_TOKEN:
        logger.info('Webhook verified successfully')
        return HttpResponse(challenge, content_type='text/plain')
    
    logger.warning('Webhook verification failed')
    return HttpResponse('Verification failed', status=403)


def handle_incoming_message(request):
    """
    Process incoming WhatsApp messages and files
    """
    try:
        body = json.loads(request.body.decode('utf-8'))
        logger.info(f'Received webhook: {json.dumps(body, indent=2)}')
        
        # Extract message data
        entry = body.get('entry', [])
        if not entry:
            return JsonResponse({'status': 'no_entry'})
        
        changes = entry[0].get('changes', [])
        if not changes:
            return JsonResponse({'status': 'no_changes'})
        
        value = changes[0].get('value', {})
        messages = value.get('messages', [])
        
        if not messages:
            return JsonResponse({'status': 'no_messages'})
        
        # Process each message
        for message in messages:
            process_message(message, value)
        
        return JsonResponse({'status': 'success'})
        
    except Exception as e:
        logger.error(f'Error handling webhook: {str(e)}', exc_info=True)
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def process_message(message, value):
    """
    Process individual WhatsApp message
    """
    try:
        message_type = message.get('type')
        from_number = message.get('from')
        
        logger.info(f'Processing message type: {message_type} from {from_number}')
        
        cv_text = None
        
        # Handle text messages
        if message_type == 'text':
            cv_text = message.get('text', {}).get('body', '')
            logger.info(f'Received text message: {cv_text[:100]}...')
        
        # Handle document (PDF) messages
        elif message_type == 'document':
            mime_type = message.get('document', {}).get('mime_type', '')
            
            if 'pdf' in mime_type.lower():
                media_id = message.get('document', {}).get('id')
                logger.info(f'Received PDF document: {media_id}')
                
                # Download the file
                file_path = whatsapp_service.download_media(media_id)
                
                if file_path:
                    # Extract text from PDF
                    cv_text = pdf_service.extract_text(file_path)
                    logger.info(f'Extracted text from PDF: {len(cv_text)} characters')
                else:
                    logger.error('Failed to download PDF file')
                    return
            else:
                logger.warning(f'Unsupported document type: {mime_type}')
                return
        
        else:
            logger.warning(f'Unsupported message type: {message_type}')
            return
        
        # Extract structured data using Gemini
        if cv_text:
            cv_data = gemini_service.extract_cv_data(cv_text)
            
            if cv_data:
                # Add WhatsApp number and timestamp
                cv_data['whatsapp_number'] = from_number
                
                # Save to Google Sheets
                sheets_service.append_cv_data(cv_data)
                
                logger.info(f'CV data saved successfully for {from_number}')
                
                # Send confirmation message
                whatsapp_service.send_message(
                    from_number,
                    f"✅ Thank you! Your CV has been received and processed.\n\n"
                    f"Name: {cv_data.get('name', 'N/A')}\n"
                    f"Email: {cv_data.get('email', 'N/A')}\n"
                    f"Phone: {cv_data.get('phone', 'N/A')}"
                )
            else:
                logger.error('Failed to extract CV data')
                whatsapp_service.send_message(
                    from_number,
                    "❌ Sorry, we couldn't process your CV. Please try again or send a different format."
                )
        
    except Exception as e:
        logger.error(f'Error processing message: {str(e)}', exc_info=True)
