"""
WSGI config for wiki_quality_web project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ["DJANGO_SETTINGS_MODULE"] = "wiki_quality_web.settings"  # see footnote [2]
_application = get_wsgi_application()


def application(environ, start_response):
    # pass the WSGI environment variables on through to os.environ
    for key in environ:
        if key.startswith('wqual_'):
            os.environ[key] = environ[key]
    os.environ["wqual_SECRET_KEY"] = "sadkoaskdopakd"
    return _application(environ, start_response)
