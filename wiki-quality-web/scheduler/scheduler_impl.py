'''
Created on 15 de dez de 2017
@author: Priscilla Raiane <priscilla.rm.carmo@gmail.com>

'''

from _datetime import datetime
from django.db import transaction
from django.db.models import Max


from scheduler.scheduler import Scheduler
from wqual.models.uploaded_datasets import Dataset, Status
from wqual.models.uploaded_datasets import StatusEnum
from wqual.models import UsedFeature


class OldestFirstScheduler(Scheduler):

	def get_next(self):
		'''
			Retorna o dataset mais antigo
		'''
		
		objSubmited = Status.objects.get_enum(StatusEnum.SUBMITTED)
		
		with transaction.atomic():
			dataset_oldest = Dataset.objects.select_for_update().filter(status=objSubmited).order_by('dat_submitted').first()
			dataset_oldest.status= Status.objects.get_enum(StatusEnum.PROCESSING)
			#atualiza a data aqui
			dataset_oldest.start_dat_processing=datetime.now()
			dataset_oldest.save()
		
		if not dataset_oldest:
			return None
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
	
	
	
	
	
	
	
	
	
	

