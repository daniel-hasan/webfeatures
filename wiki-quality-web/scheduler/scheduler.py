'''
Created on 15 de dez de 2017
@author: Priscilla Raiane <priscilla.rm.carmo@gmail.com>
'''


from abc import abstractmethod
from django.db import models, transaction
import time

from feature.features import FeatureCalculator
from scheduler.utils import DatasetModelDocReader, DatasetModelDocWriter
from wqual.models.featureset_config import UsedFeature
from wqual.models.uploaded_datasets import StatusEnum, Status

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
		while i<int_max_iterations:
			
			with transaction.atomic():
				dataset = self.get_next()
				
			print("dataset run")
			print(dataset)
			if dataset:				
				arr_feats_used = self.get_arr_features(dataset)
								
				doc_read = DatasetModelDocReader(dataset)
				doc_write = DatasetModelDocWriter()

				arr_used_feat = UsedFeature.objects.filter(feature_set_id=dataset.feature_set_id)
				
				FeatureCalculator.featureManager.computeFeatureSetDocuments(datReader=doc_read,docWriter=doc_write,arr_features_to_extract=arr_used_feat,format=dataset.format.get_enum())
				
				dataset.status = Status.objects.get_enum(StatusEnum.COMPLETE)
			else:
				time.sleep(int_wait_minutes);
				#break
			i = i+1
			
