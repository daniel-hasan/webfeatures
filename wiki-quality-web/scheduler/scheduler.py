'''
Created on 15 de dez de 2017
@author: Priscilla Raiane <priscilla.rm.carmo@gmail.com>
'''


from abc import abstractmethod
import threading
import time


from django.utils import timezone

from feature.features import FeatureCalculator
from scheduler.utils import DatasetModelDocReader, DatasetModelDocWriter
from wqual.models.featureset_config import UsedFeature
from wqual.models.uploaded_datasets import Document, DocumentText
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
	
	def run(self, int_wait_minutes,int_max_iterations = float("inf")):
		
		
		#print("AUTOCOMIT: "+str(transaction.get_autocommit()))
		int_wait_minutes = int_wait_minutes*60;
		i = 0
		bolIsSleeping = False
		#print("oioi dormindo por: "+str(int_wait_minutes))
		while i<int_max_iterations:
			bolFoundDataset = False
			if(not bolIsSleeping):
				numth = threading.get_ident()
				
			dataset=None
			with Scheduler.SCHEDULER_DATASET_LOCK:
			#print("Prox dataset...")
				dataset = self.get_next()
			
				

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
				for doc_delete in Document.objects.filter(dataset_id=dataset.id):
					if hasattr(doc_delete,"documenttext"):
						doc_delete.documenttext.delete()
					
				dataset.end_dat_processing = timezone.now()
				dataset.save()
				print("fim run \n\n")
					
			if bolFoundDataset is False:
				if not bolIsSleeping: 	
					print("dormiu")
					bolIsSleeping = True
				time.sleep(int_wait_minutes)

			i = i+1
			
