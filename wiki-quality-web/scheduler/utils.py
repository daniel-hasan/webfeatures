'''
Created on 
@author: Priscilla Raiane <priscilla.rm.carmo@gmail.com>

'''

from datetime import datetime
import json

from feature.features import Document as DocumentFeature, FeatureDocumentsReader, FeatureDocumentsWriter
from utils.basic_entities import CheckTime
from wqual.models.uploaded_datasets import Dataset, DocumentResult
from wqual.models.uploaded_datasets import SubmittedDataset, Document as DocumentDataset



class DatasetModelDocReader(FeatureDocumentsReader):
    
    def __init__(self, dataset):
        self.dataset = dataset
    
    def get_documents(self):
        
        timeToProc = CheckTime()
        i =1
        
        sub_dataset = SubmittedDataset.objects.filter(dataset=self.dataset)[0]
        arr_dsc_text = sub_dataset.grava_arq_no_dataset()
        sub_dataset.file.delete()
        sub_dataset.delete()
        for i in range(len(self.dataset.document_set.all())):   #Isso faz sentido?
            for doc in self.dataset.document_set.all():
                if hasattr(doc, "documenttext"):
                    objDocmentFeature = DocumentFeature(doc.id, doc.nam_file, arr_dsc_text[i])
                    yield objDocmentFeature
                    timeToProc.printDelta("Processing "+str(i))
                    i=i+1
                
class DatasetModelDocWriter(FeatureDocumentsWriter):
        def __init__(self, dataset):
            self.dataset = dataset
        
        def write_header(self,arr_features):
            dictFeatureHeader = {}
            for i,objFeature in enumerate(arr_features):
                dictFeatureHeader[i] = {"name":objFeature.name,
                                        "params":objFeature.get_params_str()}
                
            self.dataset.dsc_result_header = dictFeatureHeader  
            self.dataset.save()
            
        def write_document(self,document, arr_feats_used, arr_feats_result):  
            self.document = document
            self.arr_feats_used = arr_feats_used
            
            self.arr_feats_result = arr_feats_result
                                    
            doc=DocumentDataset.objects.get(id = self.document.int_doc_id)
            print("/n/n/n/nEu         aquiii o ")
            doc_result = DocumentResult(dsc_result=self.arr_feats_result, document=doc)
            doc_result.save()
            
