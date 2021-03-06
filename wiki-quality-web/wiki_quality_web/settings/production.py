# -*- coding: utf-8 -*-
"""
Arquivo de configurações (desenvolvimento) do app wqual.



For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/

"""
from wiki_quality_web.settings.development import *




#secret key and bd in  files
with open('/.wqual.cnf/s_key.txt') as f:
    SECRET_KEY = f.read().strip()

with open('/.wqual.cnf/ac.txt') as f:
    DATABASES['default']['PASSWORD'] = f.read().strip()


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [".webfeatures.com.br"]

ADMINS = (
	('Daniel Hasan Dalip', 'prof.daniel.hasan@gmail.com'),
	)
SERVER_EMAIL = "error@webfeatures.com.br"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_ROOT = "/wqual-static/"
MEDIA_ROOT = "/wqual-media/"

