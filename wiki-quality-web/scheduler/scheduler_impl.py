'''
Created on 15 de dez de 2017
@author: Priscilla Raiane <priscilla.rm.carmo@gmail.com>

'''

from _datetime import datetime
from django.db import transaction
from django.db.models import Max
import os
import threading
import time

from scheduler.scheduler import Scheduler
from wqual.models import UsedFeature
from wqual.models.uploaded_datasets import Dataset, Status
from wqual.models.uploaded_datasets import StatusEnum


class OldestFirstScheduler(Scheduler):

	
	def get_next(self):
		'''
			Retorna o dataset mais antigo
		'''
		
		
		
		numth = str(threading.get_ident())+"("+str(os.getpid())+") "
		dataset_oldest = None
		#print(str(numth)+": Pegando doc  ")
		with transaction.atomic():
			objSubmited = Status.objects.get_enum(StatusEnum.SUBMITTED)
			objProcessing = Status.objects.get_enum(StatusEnum.PROCESSING)
			
			dataset_oldest = Dataset.objects.select_for_update().filter(status=objSubmited).order_by('dat_submitted').first()
			if not dataset_oldest:
				return None
			dataset_oldest.refresh_from_db()
			print(str(numth)+": Atualizando status data set id: " + str(dataset_oldest.id)+" STATUS: "+str(dataset_oldest.status))
			dataset_oldest.status= objProcessing
			#atualiza a data aqui
			dataset_oldest.start_dat_processing=datetime.now()
			#print(str(numth)+": Salvando " + str(dataset_oldest.id))
			dataset_oldest.save()
			print(str(numth)+" Salvou o dataset: " + str(dataset_oldest.id))
			#transaction.commit()
			
			
		return dataset_oldest
	

class SchedulerSmallJobFirst(Scheduler): 

	def get_next(self):
		'''
			Retorna o dataset com o menor tempo para calcular uma feature
		'''
		used_feature_small_job = UsedFeature.objects.annotate(Max('feature_time_to_extract')).order_by('-feature_time_to_extract')[0]
		
		with transaction.atomic():
			dataset_small_job = Dataset.objects.select_for_update().filter(feature_set=used_feature_small_job.feature_set).order_by('dat_submitted')[0]
			dataset_small_job.status= Status.objects.get_enum(StatusEnum.PROCESSING)
			dataset_small_job.start_dat_processing=datetime.now()
			dataset_small_job.save()
		
		if not dataset_small_job:
			return None
		return dataset_small_job
	
	
	
	
	
	
	
	
	
	

