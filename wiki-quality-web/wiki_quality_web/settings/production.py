# -*- coding: utf-8 -*-
"""
Arquivo de configurações (desenvolvimento) do app wqual.



For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/

"""
from wiki_quality_web.settings.development import *
import os



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["www.webfeatures.com.br"]

DATABASES['default']['PASSWORD'] = os.environ['PASSWORD']


WSGI_APPLICATION = 'wiki_quality_web.wsgi.application'




# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_URL = '/static/'

STATIC_ROOT = "/home/hdalip/www/wqual/static/"

