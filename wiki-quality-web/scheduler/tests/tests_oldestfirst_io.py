'''
Created on 10/01/2018

@author: Priscilla Raiane <priscilla.rm.carmo@gmail.com>
 	Para rodar o teste pelo terminal entre na pasta wiki-quality-web
    e rode o comando:
		python3 manage.py test scheduler.tests.tests_oldestfirst_io

'''
from _datetime import datetime

from django.test.testcases import TestCase
from scheduler.scheduler_impl import OldestFirstScheduler

from django.contrib.auth.models import User
from wqual.models.uploaded_datasets import Dataset, Status, Format, StatusEnum
from wqual.models.featureset_config import FeatureSet, Language


class TestOldestScheduler(TestCase):

    def setUp(self):
        self.objFormat = Format.objects.all()[0]
        self.language = Language.objects.all()[0]
        self.status = Status.objects.all()[0]
        
        self.password = "psswd"
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
    
        next_dataset = OldestFirstScheduler().get_next()	
        
        dataset_oldest = Dataset.objects.order_by('dat_submitted').first()

        self.assertEqual(next_dataset.pk, dataset_oldest.pk, "Os datasets não são os mesmos")
        self.assertEqual(next_dataset.status, Status.objects.get_enum(StatusEnum.PROCESSING), "O status não foi atualizado")
        self.assertNotEqual(next_dataset.start_dat_processing, None, "A data de inicio do processamento não foi atualizada")




