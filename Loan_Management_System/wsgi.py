import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Loan_Management_System.settings')

application = get_wsgi_application()


try:
    call_command('migrate')  # Apply migrations
    call_command('createsuperuser', '--no-input', email='admin@example.com')  # Create superuser
except Exception as e:
    print(f"Error during startup: {e}")