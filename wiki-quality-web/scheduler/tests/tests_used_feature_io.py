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

from _datetime import datetime
from wqual.models.uploaded_datasets import Format, Dataset
from wqual.models.featureset_config import UsedFeature, UsedFeatureArgVal
import unittest



class TestUsedFeature(unittest.TestCase):
    def testL(self):
        #for usedFeature in UsedFeature.objects.all()
        self.assertEqual(0, 0, "Esse teste ainda não foi implementado")   
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'TestFeatureCalculator.testName']
    unittest.main()
        
        


