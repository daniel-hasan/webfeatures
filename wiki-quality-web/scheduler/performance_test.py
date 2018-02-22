'''
Created on 16 de fev de 2018

@author: Priscilla Raiane <priscilla.rm.carmo@gmail.com>
'''

from django.contrib.auth.models import User
from django.utils import timezone
import multiprocessing
from threading import Thread
import threading

from scheduler.scheduler_impl import OldestFirstScheduler
from wiki_quality_web.settings import BASE_DIR
from wqual.models.featureset_config import FeatureSet, Language, FeatureFactory, Feature, UsedFeature, \
    FeatureTimePerDocument, FeatureVisibility
from wqual.models.uploaded_datasets import Dataset, Format, Status


def run_scheduler():
    print("Rodando o processo...")
    OldestFirstScheduler().run(0)

class PerformanceTest(object):
    
    feature_light_id = 2
    feature_heavy_id = 3
    
    def create_feature_set(self): 
        if(User.objects.all().count()==0):
            User.objects.create_superuser('myuser', 'myemail@test.com', "secret")
        obj_english = Language.objects.get(name="en")
        arrFeatSet = FeatureSet.objects.filter(nam_feature_set = "Performance Test",user = User.objects.all()[0])
        if(len(arrFeatSet)>0):
            for objUsedFeat in arrFeatSet[0].usedfeature_set.all():
                objUsedFeat.usedfeatureargval_set.all().delete()
                objUsedFeat.delete()
            arrFeatSet[0].dataset_set.all().delete()
            arrFeatSet[0].delete()    

        obj_featureset = FeatureSet.objects.create(nam_feature_set = "Performance Test",
                                                   dsc_feature_set = "dsc_feat",
                                                   language = obj_english,  
                                                   user = User.objects.all()[0])
        
        arr_object_feature = FeatureFactory.objects.get_all_features_from_language(obj_english)
        if(len(arr_object_feature) == 0):
            FeatureFactory.objects.create(nam_module = "wqual.tests.tests_featureset_model", nam_factory_class = "FeatureFactoryDummy" )
            FeatureFactory.objects.create(nam_module = "wqual.tests.tests_featureset_model", nam_factory_class = "FeatureFactoryDummyLangDep" )            
            arr_object_feature = FeatureFactory.objects.get_all_features_from_language(obj_english)

        

        
        UsedFeature.objects.insert_features_object(featureSet=obj_featureset, 
                                                   arrObjectFeatures=arr_object_feature)
        


        return obj_featureset
        

    def create_dataset(self, num_dataset, obj_featureset):
        #mudar o caminho do arquivo USAR O BASE
        # o arquivo deve ser salvo no git?
        
        self.num_dataset = num_dataset +1
        arr_end_compress_file = []
        for i in range(11):
            #print("Base dir: "+BASE_DIR)
            arr_end_compress_file.append(BASE_DIR+"/dummy_dataset_tests/txt_"+str(i)+".zip")
       

    
        for i in range(self.num_dataset):
            objDataset = Dataset.objects.create(nam_dataset = "dataset_test"+str(i), 
                                                     dat_submitted = timezone.now(), 
                                                     dat_valid_until = timezone.datetime.strptime("2019-12-27 12:05:00", '%Y-%m-%d %H:%M:%S'), 
                                                     format = Format.objects.all()[0],
                                                     feature_set =obj_featureset,  #FeatureSet.objects.filter(id = self.feature_light_id)[0],
                                                     user = User.objects.all()[0],
                                                     status = Status.objects.all()[0])
            x=i
            if (i >= len(arr_end_compress_file)-1):
                x = i - ((i//10)*10)

            f = open(arr_end_compress_file[x], 'rb')
            objDataset.save_compressed_file(f)
            f.close() 
    

    def run_oldest_first(self, int_num_threads, int_wait_minutes=0):
        self.threads = []
        for i in range(int_num_threads +1):
            print("dentro")
            t = threading.Thread(target = OldestFirstScheduler().run(int_wait_minutes))
            print("jkjk")
            self.threads.append(t)
            t.start()
    
    def run_experiment(self, int_num_dataset, num_parallel_oldest = 2):
        arr_end_compress_files = []
        self.num_dataset = int_num_dataset
        #self.create_feature_set()
        print("antes parallel")
        #self.run_oldest_first(num_parallel_oldest)
        jobs = []
        for i in range(num_parallel_oldest):
            p = multiprocessing.Process(target=run_scheduler)
            jobs.append(p)
            p.start()
        
        #for i in range(num_parallel_oldest):
        #    t = Th(i, 0)
        #    t.start()
            
        print("dps pa")
        objFeatureSet = self.create_feature_set()
        self.create_dataset(2, objFeatureSet)
        print("Criu dataset!!! Começou diversão")

        
class Th(Thread):
    def __init__(self, num_thread, int_wait_minutes):
        Thread.__init__(self)
        self.num_thread = num_thread
        self.int_wait_minutes = int_wait_minutes
        
    def run(self):
        print(self.num_thread)
        OldestFirstScheduler().run(self.int_wait_minutes)
        
    
    
def main():
    PerformanceTest.run_experiment(7, 2)

if __name__ == "__main__":
    main()
        
        
        
        
        
        
        
        
        
        
        