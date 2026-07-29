# Copy these lines into your PythonAnywhere WSGI file, above the Django application import.
# Replace YOUR_USERNAME with your PythonAnywhere username.

import os
import sys

path = '/home/YOUR_USERNAME/khulafaa_project'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'results.settings'
os.environ['DJANGO_DEBUG'] = 'False'
os.environ['DJANGO_ALLOWED_HOSTS'] = 'YOUR_USERNAME.pythonanywhere.com'
os.environ['DJANGO_CSRF_TRUSTED_ORIGINS'] = 'https://YOUR_USERNAME.pythonanywhere.com'
os.environ['DJANGO_SECRET_KEY'] = 'replace-with-a-long-random-secret-key'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
