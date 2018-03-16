'''
Created on 13 de mar de 2018

@author: Priscilla Raiane Mendes do Carmo

from scheduler.descompress_dataset_file import *
a=DescompressDatasetFile()
a.save_dataset_docs()
'''

import os
import threading

from django.db import transaction

from wqual.models.uploaded_datasets import SubmittedDataset, Dataset, Document
import time



class DescompressDatasetFile(object):
    
    def save_dataset_docs(self, int_max_iter=float("inf"),int_wait_seconds=1):
        i = 0 
        while i<int_max_iter:
            sub_data = None
            with transaction.atomic():
                sub_data = SubmittedDataset.objects.select_for_update().order_by("dataset__dat_submitted").first()
                if(sub_data != None):
                    sub_data.grava_arq_no_dataset()
                    sub_data.file.delete()
                    sub_data.delete()
                else:
                    print(int_wait_seconds)
                    time.sleep(int_wait_seconds)
            i = i + 1
        
        
        
        