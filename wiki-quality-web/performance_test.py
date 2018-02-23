'''
Created on 16 de fev de 2018

@author: Priscilla Raiane <priscilla.rm.carmo@gmail.com>
'''


import django
import sys
from Crypto.SelfTest.Random.test__UserFriendlyRNG import multiprocessing



def create_django():
    import os
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.path.abspath(os.path.join(BASE_DIR,os.pardir))
    
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wiki_quality_web.settings")
    #adiciona o projeto wiki-quality como dependente 
    sys.path.append(os.path.join(BASE_DIR,"wiki-quality"))
    print("WIJIQUALITY: "+os.path.join(BASE_DIR,"wiki-quality"))
    django.setup()
        
def run_scheduler():
    create_django()
    from scheduler.scheduler_impl import OldestFirstScheduler
    OldestFirstScheduler().run(0)




        

        
def create_database():
    create_django()
    from scheduler.performance_test.dataset_creator import PerformanceTest    
    p = PerformanceTest()
    objFeatureSet = p.create_feature_set()
    p.create_dataset(5, objFeatureSet)
        


if __name__ == "__main__":
    #create_database()
    for i in range(2):
        t = multiprocessing.Process(target = run_scheduler)
        t.start()
    
        
        
        
        
        
        
        
        
        
        
        