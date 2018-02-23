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
		
		#print(str(numth)+": Pegando doc  ")

		idDataset = None
		
		#print("Nova pesquisa...")
		objSubmited = Status.objects.get_enum(StatusEnum.SUBMITTED)
		objProcessing = Status.objects.get_enum(StatusEnum.PROCESSING)
			
		with transaction.atomic():
			dataset_oldest = Dataset.objects.select_for_update().filter(status=objSubmited).order_by('dat_submitted').first()
			if not dataset_oldest:
				return None
					#dataset_oldest.refresh_from_db()
			dataset_oldest.status= objProcessing
			dataset_oldest.start_dat_processing=datetime.now()
			print(str(numth)+": Salvando " + str(dataset_oldest.id))
			dataset_oldest.save()
		
		dataset_oldest_prox = Dataset.objects.filter(status=objSubmited).order_by('dat_submitted').first()
		if(dataset_oldest_prox!=None):
			objDataset = Dataset.objects.get(id=dataset_oldest_prox.id)
			print(str(numth)+": O proxiiiimo é: "+str(dataset_oldest_prox.id)+" STATUS: "+str(objDataset.status))
		#else:
		#	objDataset = Dataset.objects.get(id=dataset_oldest.id)
		#	print(str(numth)+": Nao achou mais proximo :( ultimo status: "+objDataset.status.name)
		#print("SUBMITED: "+str(objSubmited.id))
		#print("PROCESSING: "+str(objProcessing.id))
		
		#dataset_oldest_prox = Dataset.objects.filter(status=objSubmited).order_by('dat_submitted').first()
		#if(dataset_oldest_prox!=None):
		#	objDataset = Dataset.objects.get(id=dataset_oldest_prox.id)
		#	print(str(numth)+": O prox é: "+str(dataset_oldest_prox.id)+" STATUS: "+str(objDataset.status))
						
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
	
	
	
	
	
	
	
	
	
	

