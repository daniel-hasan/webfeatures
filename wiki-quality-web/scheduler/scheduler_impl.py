'''
Created on 15 de dez de 2017
@author: Priscilla Raiane <priscilla.rm.carmo@gmail.com>

'''
from django.db import transaction

from scheduler.scheduler import Scheduler
from wqual.models.uploaded_datasets import Dataset, Status
from wqual.models.uploaded_datasets import StatusEnum

class OldestFirstScheduler(Scheduler):

	def get_next(self):
		objSubmited = Status.objects.get_enum(StatusEnum.SUBMITTED)

		with transaction.atomic():
			dataset_oldest = Dataset.objects.select_for_update().filter(status=objSubmited).order_by('dat_submitted').first()
			dataset_oldest.status= Status.objects.get_enum(StatusEnum.PROCESSING)
			#atualiza a data aqui
			dataset_oldest.save()

		if not dataset_oldest:
			return None
		return dataset_oldest


