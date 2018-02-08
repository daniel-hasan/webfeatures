import json

from feature.features import Document as DocumentFeature, FeatureDocumentsReader, FeatureDocumentsWriter
from wqual.models.uploaded_datasets import Dataset, DocumentResult
from wqual.models.uploaded_datasets import Document as DocumentDataset


class DatasetModelDocReader(FeatureDocumentsReader):
    
    def __init__(self, dataset):
        self.dataset = dataset
    
    def get_documents(self):
        
        for doc in self.dataset.document_set.all():
          
            yield DocumentFeature(doc.id, doc.nam_file, doc.documenttext.dsc_text)
            
class DatasetModelDocWriter(FeatureDocumentsWriter):
        
        def write_document(self,document, arr_feats_used, arr_feats_result):    
            self.document = document
            self.arr_feats_used = arr_feats_used
            self.arr_feats_result = json.dumps(arr_feats_result)
            
            doc=DocumentDataset.objects.get(id = self.document.int_doc_id)
            doc_result = DocumentResult(dsc_result=arr_feats_result, document=doc)
            doc_result.save()
            
