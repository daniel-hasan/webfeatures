'''
Created on 30 de jan de 2018

@author: Priscilla Raiane <priscilla.rm.carmo@gmail.com>

comando para rodar o test:
    python3 manage.py shell < tests_run_usedfeature.py

'''

try:
    from django.core.management.base import NoArgsCommand as BaseCommand
except ImportError:
    from django.core.management.base import BaseCommand

from django.core.management.base import BaseCommand
import sys
import argparse

from scheduler.tests.tests_used_feature_io import TestUsedFeature

TestUsedFeature().testL()

