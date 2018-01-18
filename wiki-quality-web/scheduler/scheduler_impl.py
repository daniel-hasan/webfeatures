from django.db import transaction

from scheduler.Scheduler import Scheduler
from wqual.models.uploaded_datasets import Dataset, Status
from wqual.models.uploaded_datasets import StatusEnum
 

class OldestFirstScheduler(Scheduler):

	def get_next(self):

		with transaction.atomic():
			objSubmited = Status.objects.get_enum(StatusEnum.SUBMITTED)
			dataset_oldest = Dataset.objects.select_for_update().filter(status=objSubmited).order_by('dat_submitted').first()
			# erra só isso: dataset_oldest = Dataset.objects.filter(status=objSubmited).order_by('dat_submitted').first()
			if not dataset_oldest:
				return None
			return dataset_oldest


