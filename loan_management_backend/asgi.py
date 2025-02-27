import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loan_management_backend.settings')

print("Starting ASGI application...")  # Debug log
application = get_asgi_application()
