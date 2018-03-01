'''
Created on 15 de dez de 2017
@author: Priscilla Raiane <priscilla.rm.carmo@gmail.com>

'''

from django.db import transaction
from django.db.models import Max
from django.utils import timezone
import os
import threading

from scheduler.scheduler import Scheduler
from wqual.models import UsedFeature
from wqual.models.uploaded_datasets import Dataset, Status
from wqual.models.uploaded_datasets import StatusEnum


class OldestFirstScheduler(Scheduler):

	
	def get_next(self):
		'''
			Retorna o dataset mais antigo
		'''
		
		
		
		#numth = str(threading.get_ident())+"("+str(os.getpid())+"): "
		numth = str(os.getpid())+": "
		
		

		#para evitar bloquear muito a tabela, caso nao tenha dataset, sair
		
		
		dataset_oldest = None
		objSubmited = Status.objects.get_enum(StatusEnum.SUBMITTED)
		objProcessing = Status.objects.get_enum(StatusEnum.PROCESSING)
		#transaction.set_autocommit(False)
	
		with transaction.atomic():
			
			dataset_oldest = Dataset.objects.select_for_update().filter(status=objSubmited,bol_ready_to_process=True).order_by('dat_submitted').first()
			
			if not dataset_oldest:
				return None

			dataset_oldest.status= objProcessing
			dataset_oldest.start_dat_processing=timezone.now()
			dataset_oldest.num_proc_extractor = os.getpid() 
			dataset_oldest.save()

						
		return dataset_oldest
	

class SchedulerSmallJobFirst(Scheduler): 

	def get_next(self):
		'''
			Retorna o dataset com o menor tempo para calcular uma feature
		'''
		used_feature_small_job = UsedFeature.objects.annotate(Max('feature_time_to_extract')).order_by('-feature_time_to_extract')[0]
		
		with transaction.atomic():
			dataset_small_job = Dataset.objects.select_for_update().filter(feature_set=used_feature_small_job.feature_set,bol_ready_to_process=True).order_by('dat_submitted')[0]
			dataset_small_job.status= Status.objects.get_enum(StatusEnum.PROCESSING)
			dataset_small_job.start_dat_processing=timezone.now()
			dataset_small_job.save()
		
		if not dataset_small_job:
			return None
		return dataset_small_job
	
	
	
	
	
	
	
	
	
	

