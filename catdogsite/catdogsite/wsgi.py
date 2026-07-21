import os
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catdogsite.settings')

# Automatically run database migrations on startup for production/Render
try:
    call_command('migrate')
except Exception as e:
    print(f"Migration error: {e}")

application = get_wsgi_application()