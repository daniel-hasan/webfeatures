"""
WSGI config for wiki_quality_web project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys
import site
from django.core.wsgi import get_wsgi_application

#os.environ["wqual_SECRET_KEY"] = "XXXXXXXXXX"
#os.environ["wqual_db_PASSWORD"] = "XXXXXXXXXX"

#adiciona o projeto wiki-quality como dependente 
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#strFile = os.path.join(BASE_DIR,"git/wiki-quality/wiki-quality")
#site.addsitedir(strFile);
#if(not os.path.isdir(strFile)):
#        raise Exception("Nao achou o diretorio:"+strFile)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wiki_quality_web.settings")


application = get_wsgi_application()

