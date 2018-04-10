'''
Created on 30/10/2017

@author: Priscilla
    Teste unitario das classes DatasetModelDocReader e DatasetModelDocWriter
    
    Para rodar o teste pelo terminal entre na pasta wiki-quality-web
    e rode o comando:
            python3 manage.py test scheduler.tests.tests_doc_io


'''
import json
import os

from django.contrib.auth.models import User
from django.core.files import uploadedfile
from django.test.testcases import TestCase
from django.utils import timezone

from feature.features import Document as DocumentFeature
from scheduler.utils import DatasetModelDocReader, DatasetModelDocWriter
from wqual.models.featureset_config import FeatureSet, Language
from wqual.models.uploaded_datasets import Dataset, Format, Status, \
    SubmittedDataset
from wqual.models.uploaded_datasets import Document as DocumentDataset

from django.http import HttpResponseRedirect
from django.shortcuts import render

from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

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
                                                 dat_submitted = timezone.now(), 
                                                 dat_valid_until = timezone.now(), 
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
            doc.delete()
            
        self.objDataset.delete()
        self.feature_set.delete()
        self.my_admin.delete()
    
    '''      
            
    def testReader(self):
        my_base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/dummy_dataset_tests/txt_2.zip"
        #<class 'django.core.files.uploadedfile.InMemoryUploadedFile'>
        f = UploadFileForm(request.POST, request.FILES)
        
        with open(my_base_dir, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
                
        destination
        '''
        d = DatasetModelDocReader(dataset=self.objDataset)
        print(my_base_dir)
        #for i in range(10):
        f = open (my_base_dir, "rb");
        SubmittedDataset.objects.create(dataset=self.objDataset, file=f)
        
        
        for doc in d.get_documents():
            bol_encontrou = False
            for docCriado in self.arrDocs:
                if(doc.int_doc_id == docCriado.id):
                    bol_encontrou = True
                    self.assertEqual(doc.str_doc_name, docCriado.nam_file, "O nome do arquivo não esta igual!")
                    #self.assertEqual(doc.str_text, docCriado.documenttext.dsc_text, "O nome do arquivo não esta igual!")
                    
            self.assertTrue(bol_encontrou, "Nao foi possivel encontrar o documento de id: "+str(doc.int_doc_id)+" nome: "+doc.str_doc_name)
        '''
    '''
    def testWriter(self):
        d = DatasetModelDocWriter(self.objDataset)
        arr_feats_used = ["Texto das features usadas"]
        arr_feats_result = [{'Teste': 'feat1', 'teste2': 'feat2'}] #
                
        for doc_feat in self.arr_doc_feat:
            d.write_document(doc_feat, arr_feats_used, arr_feats_result)

            self.assertEqual(doc_feat.int_doc_id, DocumentDataset.objects.get(id = doc_feat.int_doc_id).id, 
                                   "Nao foi possivel encontrar o documento com o id procurado")
        
            self.assertEqual(arr_feats_result, json.loads(DocumentDataset.objects.get(id = doc_feat.int_doc_id).documentresult.dsc_result), 
                                   "O dsc_result não é igual ao resultado do documento com o id proucurado")
            
                
    
    '''
            