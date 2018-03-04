'''
Created on 16 de fev de 2018

@author: Priscilla Raiane <priscilla.rm.carmo@gmail.com>
'''
import django
import sys





user_name = "__perf_test__"
nam_feature_set = "Performance Test\t{num_dataset}\t{num_proc}"
output_result = "performance_output.xls"

def create_django():
    import os
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    BASE_DIR = os.path.abspath(os.path.join(BASE_DIR,os.pardir))
    
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wiki_quality_web.settings")
    #adiciona o projeto wiki-quality como dependente 
    sys.path.append(os.path.join(BASE_DIR,"wiki-quality"))
    print("WIKIQUALITY: "+os.path.join(BASE_DIR,"wiki-quality"))
    django.setup()
        
def run_scheduler():
    create_django()
    from scheduler.scheduler_impl import OldestFirstScheduler
    OldestFirstScheduler().run(1)

def get_performance_featureset_name(int_num_processes,int_num_datasets):
    return nam_feature_set.format(num_proc=int_num_processes,num_dataset=int_num_datasets)
def write_performance_test():
    create_django()
    from wqual.models import FeatureSet
    from wqual.models.uploaded_datasets import StatusEnum
    
    
    with open(output_result,"w") as f:
        f.write("FeatSetName\t#datasets(expected)\t#schedulers\t#datasets(real)\tTotal Proc. Time\tAvg. Proc time per dataset\tMax Proc. Time\tMin Proc. Time\t"+
                        "Doc. count\tAvg. doc per dataset\n")
        for featSet in FeatureSet.objects.filter(user__username=user_name):
            arrDatIncomplete = []
            arrDatasets = list(featSet.dataset_set.all().order_by("start_dat_processing"))
            
            
            first_start_processing = None
            last_end_dat_processing = None
            max_processing = None
            min_processing = None
            sumDocumentCount = None
            
            #verifica se o primeiro esta completo
            if arrDatasets[0].status.get_enum() != StatusEnum.COMPLETE:
                arrDatIncomplete.append(arrDatasets[0].nam_dataset)
                
            else:
                first_start_processing = arrDatasets[0].start_dat_processing
                last_end_dat_processing = arrDatasets[0].end_dat_processing
                max_processing = arrDatasets[0].end_dat_processing-arrDatasets[0].start_dat_processing
                min_processing = arrDatasets[0].end_dat_processing-arrDatasets[0].start_dat_processing
                sumDocumentCount = arrDatasets[0].document_set.all().count()
            

            for dataset in arrDatasets:
                
                 
                #verifica se o dataset esta completo
                if dataset.status.get_enum() != StatusEnum.COMPLETE:
                    arrDatIncomplete.append(arrDatasets[0].nam_dataset)
                    
                if(len(arrDatIncomplete)==0):
                    cur_processing = dataset.end_dat_processing-dataset.start_dat_processing
                    if(max_processing<cur_processing):
                        max_processing = cur_processing
                    if(min_processing>cur_processing):
                        min_processing = cur_processing
                    sumDocumentCount += dataset.document_set.all().count()
                    #verifica se o processamento dele foi posterior ao last_end_dat_processing
                    if(last_end_dat_processing<dataset.end_dat_processing):
                        last_end_dat_processing = dataset.end_dat_processing
    
            
            
            if(len(arrDatIncomplete)>0):
                f.write(featSet.nam_feature_set+"\tThese datasets are incomplete: "+"; ".join(arrDatIncomplete))
            else:
                sec_total_processing = (last_end_dat_processing-first_start_processing).total_seconds()
                sec_max_processing = max_processing.total_seconds()
                sec_min_processing = min_processing.total_seconds()
                avg_documents_per_dataset = sumDocumentCount/len(arrDatasets)
                avg_time_per_dataset = sec_total_processing/len(arrDatasets)
                num_datasets = len(arrDatasets)
                f.write(featSet.nam_feature_set+"\t"+str(num_datasets)+"\t"+str(sec_total_processing)+"\t"+str(avg_time_per_dataset)+"\t"+str(sec_max_processing)+"\t"+str(sec_min_processing)+
                        "\t"+str(sumDocumentCount)+"\t"+str(avg_documents_per_dataset))
                
            f.write("\n")
    print("Datasets processing statistics saved in: "+output_result)

        
def create_database(int_num_processes,int_num_datasets):
    create_django()
    from scheduler.performance_test.dataset_creator import PerformanceTest    
    p = PerformanceTest()
    
    objFeatureSet = p.create_feature_set(user_name, get_performance_featureset_name(int_num_processes,int_num_datasets))
    p.create_dataset(int_num_datasets, objFeatureSet)
        



        
        
    
        
        
        
        
        
        
        
        
        
        
        