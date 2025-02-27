import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loan_management_backend.settings')

print("Starting WSGI application...")  # Debug log
application = get_wsgi_application()
