'''
Created on 24 de jan de 2018

@author: Priscilla Raiane

Erros encontrados
executar o comando:  export DJANGO_SETTINGS_MODULE=wiki_quality_web.settings
se algum não estiver instalado arquivo: pip3 install django-extensions

para rodar:  python3 manage.py shell < scheduler/tests/tests_UsedFeature_io.py 

'''

#from django.test.testcases import TestCase

from django.template import Template, Context
from django.conf import settings

from django.utils import timezone
from wqual.models.uploaded_datasets import Format, Dataset
from wqual.models.featureset_config import UsedFeature, UsedFeatureArgVal
import unittest



class TestUsedFeature(unittest.TestCase):
    def testL(self):
        for used_feature in UsedFeature.objects.all():
            feat_inst = used_feature.get_feature_instance()

        


