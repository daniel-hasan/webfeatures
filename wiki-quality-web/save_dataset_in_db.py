'''
Created on 14 de mar de 2018

@author: Priscilla Raiane
'''

import sys

import django

from scheduler.performance_test.performance_test import create_django
    
if __name__ == '__main__':
    create_django()
    from scheduler.descompress_dataset_file import DescompressDatasetFile
    DescompressDatasetFile().save_dataset_docs()
