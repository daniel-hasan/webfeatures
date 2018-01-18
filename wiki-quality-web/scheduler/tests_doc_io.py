'''
Created on 30/10/2017

@author: Priscilla
    Teste unitario das classes DatasetModelDocReader e DatasetModelDocWriter
    
    Para rodar o teste pelo terminal entre na pasta wiki-quality-web
    e rode o comando:
            python3 manage.py test scheduler.tests_doc_io


'''
from _datetime import datetime

from django.contrib.auth.models import User
from django.test.testcases import TestCase

from scheduler.utils import DatasetModelDocReader, DatasetModelDocWriter
from wqual.models.featureset_config import FeatureSet, Language
from wqual.models.uploaded_datasets import Dataset, Format, DocumentText, Status
from feature.features import Document as DocumentFeature
from wqual.models.uploaded_datasets import Document as DocumentDataset
import json


class TestDocIO(TestCase):
    
    def setUp(self):

        Format.objects.update_enums_in_db()
        Language.objects.update_enums_in_db()
        Status.objects.update_enums_in_db()
        
        self.objFormat = Format.objects.all()[0]
        self.language = Language.objects.all()[0]
        self.status = Status.objects.all()[0]
        
        self.password = "meunome"
        self.my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', self.password)
        self.feature_set = FeatureSet.objects.create(nam_feature_set="Featzinho",
                                                     dsc_feature_set="lalalal",
                                                     language=self.language,
                                                     user=self.my_admin)
        
        self.objDataset = Dataset.objects.create(nam_dataset = "dataset_test", 
                                                 dat_submitted = datetime.now(), 
                                                 dat_valid_until = datetime.now(), 
                                                 format = self.objFormat,
                                                 feature_set=self.feature_set,
                                                 user=self.my_admin,
                                                 status=self.status)
        self.arrDocs = []
        self.arr_doc_feat = []

        for i in range(10):
            self.arrDocs.append(DocumentDataset.objects.create(nam_file = "doc_read_teste" +str(i), dataset = self.objDataset))
            self.arr_doc_feat.append(DocumentFeature(int_doc_id= self.arrDocs[i].id, str_doc_name="doc_name" +str(i), str_text="texto"))

    '''        
    def tearDown(self):
        for doc in self.arrDocs:
            doc.documenttext.delete()
            doc.delete()
            
        self.objDataset.delete()
        self.feature_set.delete()
        self.my_admin.delete()
    
    
    def testReader(self):
        d = DatasetModelDocReader(dataset=self.objDataset)

        for i in range(10):
            DocumentText.objects.create(dsc_text = "Insira um texto aqui", document =self.arrDocs[i])
        
        for doc in d.get_documents():
            bol_encontrou = False
            for docCriado in self.arrDocs:
                if(doc.int_doc_id == docCriado.id):
                    bol_encontrou = True
                    self.assertEqual(doc.str_doc_name, docCriado.nam_file, "O nome do arquivo não esta igual!")
                    self.assertEqual(doc.str_text, docCriado.documenttext.dsc_text, "O nome do arquivo não esta igual!")
                    
            self.assertTrue(bol_encontrou, "Nao foi possivel encontrar o documento de id: "+str(doc.int_doc_id)+" nome: "+doc.str_doc_name)
    '''

    

    def testWriter(self):
        d = DatasetModelDocWriter()
        arr_feats_used = ["Texto das features usadas"]
        arr_feats_result = ['texto do resultado das features']        
        
        '''
        for doc_feat in self.arr_doc_feat:
        '''

        doc_feat=self.arr_doc_feat[0]
        d.write_document(doc_feat, arr_feats_used, arr_feats_result)
        self.assertEqual(1, 1, Ok)

        '''
            self.assertEqual(doc_feat.int_doc_id, DocumentDataset.objects.get(id = doc_feat.int_doc_id).id, 
                                   "Nao foi possivel encontrar o documento com o id procurado")
        
            self.assertEqual(str(arr_feats_result), (DocumentDataset.objects.get(id = doc_feat.int_doc_id).documentresult.dsc_result), 
                                   "O dsc_result não é igual ao resultado do documento com o id proucurado")
            
        '''        
    
    
