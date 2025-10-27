"""
WSGI config for CV Manager project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cv_manager.settings')

application = get_wsgi_application()
