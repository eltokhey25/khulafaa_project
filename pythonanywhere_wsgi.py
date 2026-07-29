# =====================================================================
# PythonAnywhere WSGI Configuration File
# =====================================================================
# HOW TO USE:
#   1. Copy the CONTENTS of this file.
#   2. Go to Web tab on PythonAnywhere → click the WSGI configuration file link.
#   3. Delete everything and paste this content.
#   4. Replace YOUR_USERNAME with your PythonAnywhere username.
#   5. Replace PASTE_YOUR_SECRET_KEY_HERE with a real secret key.
#      Generate one with:
#        python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
# =====================================================================

import os
import sys

# --- Project path ---
path = '/home/YOUR_USERNAME/khulafaa_project'
if path not in sys.path:
    sys.path.insert(0, path)

# --- Environment variables ---
os.environ['DJANGO_SETTINGS_MODULE'] = 'results.settings'
os.environ['DJANGO_DEBUG'] = 'False'
os.environ['DJANGO_ALLOWED_HOSTS'] = 'YOUR_USERNAME.pythonanywhere.com'
os.environ['DJANGO_CSRF_TRUSTED_ORIGINS'] = 'https://YOUR_USERNAME.pythonanywhere.com'
os.environ['DJANGO_SECRET_KEY'] = 'PASTE_YOUR_SECRET_KEY_HERE'

# --- WSGI application ---
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
