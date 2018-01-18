'''
Created on 10/01/2018

@author: Priscilla

'''
from _datetime import datetime

from django.test.testcases import TestCase
from scheduler.scheduler import Scheduler
from scheduler.scheduler_impl import OldestFirstScheduler

from wqual.models.uploaded_datasets import Dataset, Status
from wqual.models.uploaded_datasets import StatusEnum


class TestOldestScheduler(TestCase):
	self.objFormat = Format.objects.all()[0]
    self.language = Language.objects.all()[0]
    self.status = Status.objects.all()[0]
        
    self.password = "senha"
    self.my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', self.password)
    self.feature_set = FeatureSet.objects.create(nam_feature_set="Featzinho",
                                                dsc_feature_set="lalalal",
                                                language=self.language,
                                                user=self.my_admin)
        
    date0 = datetime(2018, 3, 27, 12, 5, 14, 0)
    date1 = datetime(2018, 3, 27, 12, 5, 34, 0)
    date2 = datetime(2018, 3, 27, 12, 5, 55, 0)

    self.objDataset0 = Dataset.objects.create(nam_dataset = "dataset_test0", 
                                                dat_submitted = date0, 
                                                dat_valid_until = datetime.now(), 
                                                format = self.objFormat,
                                                feature_set=self.feature_set,
                                                user=self.my_admin,
                                                status=self.status)

    self.objDataset1 = Dataset.objects.create(nam_dataset = "dataset_test1", 
                                                dat_submitted = date1, 
                                                dat_valid_until = datetime.now(), 
                                                format = self.objFormat,
                                                feature_set=self.feature_set,
                                                user=self.my_admin,
                                                status=self.status)

    self.objDataset2 = Dataset.objects.create(nam_dataset = "dataset_test2", 
                                                dat_submitted = date2, 
                                                dat_valid_until = datetime.now(), 
                                                format = self.objFormat,
                                                feature_set=self.feature_set,
                                                user=self.my_admin,
                                                status=self.status)

'''
def tearDown(self):
'''

def testOldest(self):

	#scheduler_get_next = #como chamar??

	objSubmited = Status.objects.get_enum(StatusEnum.SUBMITTED)
	dataset_oldest = Dataset.objects.filter(status=objSubmited).order_by('dat_submitted').first()

	self.assertEqual(scheduler_get_next, dataset_oldest, "Os datasets não são os mesmos")
