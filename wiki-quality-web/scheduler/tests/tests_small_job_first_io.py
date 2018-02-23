'''
Created on 31 de jan de 2018

@author: Priscilla Raiane <priscilla.rm.carmo@gmail.com>

'''

from django.utils import timezone

from django.test.testcases import TestCase
from scheduler.scheduler_impl import SchedulerSmallJobFirst
from django.db.models import Max

from django.contrib.auth.models import User
from wqual.models.uploaded_datasets import Dataset, Status, Format, StatusEnum
from wqual.models.featureset_config import FeatureSet, Language
from wqual.models.featureset_config import UsedFeature, Feature, FeatureTimePerDocument, FeatureVisibility


class TestOldestScheduler(TestCase):

    def setUp(self):
        self.objFormat = Format.objects.all()[0]
        self.language = Language.objects.all()[0]
        self.status = Status.objects.all()[0]
        
        self.password = "psswd"
        self.my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', self.password)
        self.feature_set = FeatureSet.objects.create(nam_feature_set="Small_Job",
                                                    dsc_feature_set="dsc_feature",
                                                    language=self.language,
                                                    user=self.my_admin)
        
        self.feature_set1 = FeatureSet.objects.create(nam_feature_set="Small_Job_1",
                                                    dsc_feature_set="dsc_feature_2",
                                                    language=self.language,
                                                    user=self.my_admin)
        
        date0 = datetime(2018, 3, 27, 12, 5, 14, 0)
        date1 = datetime(2018, 3, 27, 12, 5, 34, 0)
        date2 = datetime(2018, 3, 27, 12, 5, 55, 0)
        
        self.objDataset0 = Dataset.objects.create(nam_dataset = "dataset_test0", 
                                                    dat_submitted = date0, 
                                                    dat_valid_until = timezone.now(), 
                                                    format = self.objFormat,
                                                    feature_set=self.feature_set,
                                                    user=self.my_admin,
                                                    status=self.status)
        
        self.objDataset1 = Dataset.objects.create(nam_dataset = "dataset_test1", 
                                                    dat_submitted = date1, 
                                                    dat_valid_until = timezone.now(),
                                                    format = self.objFormat,
                                                    feature_set=self.feature_set1,
                                                    user=self.my_admin,
                                                    status=self.status)
        
        self.objDataset2 = Dataset.objects.create(nam_dataset = "dataset_test2", 
                                                    dat_submitted = date2, 
                                                    dat_valid_until = timezone.now(), 
                                                    format = self.objFormat,
                                                    feature_set=self.feature_set,
                                                    user=self.my_admin,
                                                    status=self.status)    
        
        self.objFeature = Feature.objects.create(nam_module = 'nam_module', nam_feature_class = 'nam_feature_class')
        
        self.objUsedFeature = []
        self.objUsedFeature.append( UsedFeature.objects.create(ord_feature = 1, feature_set = self.feature_set,
                                                         feature = self.objFeature,
                                                         feature_time_to_extract = FeatureTimePerDocument.objects.all()[3],     
                                                         feature_visibility = FeatureVisibility.objects.all()[0],
                                                         text_format = self.objFormat
                                                         ))
        
        self.objUsedFeature.append( UsedFeature.objects.create(ord_feature = 1, feature_set = self.feature_set1,
                                                         feature = self.objFeature,
                                                         feature_time_to_extract = FeatureTimePerDocument.objects.all()[3],     
                                                         feature_visibility = FeatureVisibility.objects.all()[0],
                                                         text_format = self.objFormat
                                                         ))
        
        self.objUsedFeature.append( UsedFeature.objects.create(ord_feature = 1, feature_set = self.feature_set,
                                                         feature = self.objFeature,
                                                         feature_time_to_extract = FeatureTimePerDocument.objects.all()[4],     
                                                         feature_visibility = FeatureVisibility.objects.all()[0],
                                                         text_format = self.objFormat
                                                         ))
        
        
    def testSmallJob(self):
        next_dataset = SchedulerSmallJobFirst().get_next()
        
        small_job_dataset = Dataset.objects.all().filter(feature_set = 
                                                        UsedFeature.objects.all().order_by('-feature_time_to_extract')[0].feature_set).order_by('dat_submitted')[0]
        
        self.assertEqual(next_dataset.pk, small_job_dataset.pk, "O dataset retornado não possui a feature de menor tempo")
        self.assertNotEqual(next_dataset.start_dat_processing, None, "A data de inicio de processamento não foi atualizada")
        
        
        