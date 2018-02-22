'''
Created on 15 de dez de 2017
@author: Priscilla Raiane <priscilla.rm.carmo@gmail.com>
'''


from abc import abstractmethod
from django.db import models, transaction
import time
from django.utils import timezone


from feature.features import FeatureCalculator
from scheduler.utils import DatasetModelDocReader, DatasetModelDocWriter
from wqual.models.featureset_config import UsedFeature
from wqual.models.uploaded_datasets import StatusEnum, Status
from wqual.models.uploaded_datasets import Document, DocumentText

class Scheduler(object):

	@abstractmethod
	def get_next(self):
		pass
	
	def get_arr_features(self,dataset):
		arrUsedFeatures = UsedFeature.objects.filter(feature_set_id=dataset.feature_set_id).order_by("ord_feature")
		arrFeatures = []
		for objUsedFeature in arrUsedFeatures:
			arrFeatures.append(objUsedFeature.get_feature_instance())
		return arrFeatures
	
	def run(self, int_wait_minutes,int_max_iterations = float('inf')):
				
		int_wait_minutes = int_wait_minutes*60;
		i = 0
		bolIsSleeping = True
		while i<int_max_iterations:
			bolFoundDataset = False

			dataset = self.get_next()
				
			if dataset:
				print("Peguei o dateaset: " + dataset.nam_dataset)
				print("OI tudo bom")
				bolIsSleeping = False
				bolFoundDataset = True				
				arr_feats_used = self.get_arr_features(dataset)
									
				doc_read = DatasetModelDocReader(dataset)
				doc_write = DatasetModelDocWriter(dataset)

				FeatureCalculator.featureManager.computeFeatureSetDocuments(datReader=doc_read,docWriter=doc_write,arr_features_to_extract=arr_feats_used,format=dataset.format.get_enum())
					
				dataset.status = Status.objects.get_enum(StatusEnum.COMPLETE)
					
					
				for doc_delete in Document.objects.filter(dataset_id=dataset.id):
					if doc_delete.documenttext != None:
						doc_delete.documenttext.delete()
					
				dataset.end_dat_processing = timezone.now()
				dataset.save()
				print("fim run \n\n")
					
			if bolFoundDataset is False:
				if not bolIsSleeping: 	
					print("dormiu")
					bolIsSleeping = True
				time.sleep(int_wait_minutes);

			i = i+1
			
