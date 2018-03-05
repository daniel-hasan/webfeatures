"""
WSGI config for wiki_quality_web project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ["wqual_SECRET_KEY"] = "XXXXXXXXXX"
os.environ["wqual_db_PASSWORD"] = "XXXXXXXXXX"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wiki_quality_web.settings")


application = get_wsgi_application()
