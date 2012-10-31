import sys
import os.path

# manage.py is automatically created in each Django project. manage.py is a thin
# wrapper around django-admin.py that takes care of two things for you before 
# delegating to django-admin.py:
#
#   It puts your project's package on sys.path.
#   It sets the DJANGO_SETTINGS_MODULE environment variable so that it points to 
#   your project's settings.py file.
#
# ref: https://docs.djangoproject.com/en/1.4/ref/django-admin/

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
sys.path.append(os.path.join(os.path.dirname(__file__), 'mysite'))

import sae
import django.core.handlers.wsgi

application = sae.create_wsgi_app(django.core.handlers.wsgi.WSGIHandler())
