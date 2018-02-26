'''
Created on 15 de dez de 2017
@author: Priscilla Raiane <priscilla.rm.carmo@gmail.com>
'''


from abc import abstractmethod
from datetime import datetime
from django.utils import timezone
import os
import threading
import time

from feature.features import FeatureCalculator
from scheduler.utils import DatasetModelDocReader, DatasetModelDocWriter
from wqual.models.featureset_config import UsedFeature
from wqual.models.uploaded_datasets import Document, DocumentText, Dataset
from wqual.models.uploaded_datasets import StatusEnum, Status


class Scheduler(object):
	SCHEDULER_DATASET_LOCK = threading.Lock()
	
	@abstractmethod
	def get_next(self):
		pass
	
	def get_arr_features(self,dataset):
		arrUsedFeatures = UsedFeature.objects.filter(feature_set_id=dataset.feature_set_id).order_by("ord_feature")
		arrFeatures = []
		for objUsedFeature in arrUsedFeatures:
			arrFeatures.append(objUsedFeature.get_feature_instance())
		return arrFeatures
	def is_onwer(self,dataset):
		pass
	def run(self, int_wait_seconds,int_max_iterations = float("inf")):
		numth = str(threading.get_ident())+"("+str(os.getpid())+") "
		objSubmited = Status.objects.get_enum(StatusEnum.SUBMITTED)
		#print("AUTOCOMIT: "+str(transaction.get_autocommit()))
		
		i = 0
		bolIsSleeping = False
		#print("oioi dormindo por: "+str(int_wait_minutes))
		while i<int_max_iterations:
			bolFoundDataset = False
				
			dataset=None
			
			#print("Prox dataset...")
			while dataset == None or dataset.num_proc_extractor!=os.getpid():
				dataset = self.get_next()
				if(dataset != None):
					dataset.refresh_from_db()
					dataset = Dataset.objects.get(id = dataset.id)
				else:
					while(Dataset.objects.filter(status=objSubmited).count()==0):
						time.sleep(int_wait_seconds)
				

			if dataset:
				#print("Peguei o dateaset: " + dataset.nam_dataset)
				bolIsSleeping = False
				bolFoundDataset = True				
				arr_feats_used = self.get_arr_features(dataset)
									
				doc_read = DatasetModelDocReader(dataset)
				doc_write = DatasetModelDocWriter(dataset)

				FeatureCalculator.featureManager.computeFeatureSetDocuments(datReader=doc_read,docWriter=doc_write,arr_features_to_extract=arr_feats_used,format=dataset.format.get_enum())
					
				dataset.status = Status.objects.get_enum(StatusEnum.COMPLETE)
					
				#delete os textos do doc
				DocumentText.objects.filter(document__dataset_id=dataset.id).delete()
				
					
				dataset.end_dat_processing = timezone.now()
				timeDeltaProc = dataset.end_dat_processing-dataset.start_dat_processing
				dataset.save()
				print(str(numth)+": Dataset '"+dataset.nam_dataset+"' processed in "+str(timeDeltaProc))
					

			i = i+1
			
