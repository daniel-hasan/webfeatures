'''
Created on 28 de jun de 2018

@author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
Views relacionadas a criação do dataset
'''
import json
import os.path
import uuid

from django.contrib.auth.models import User
from django.core.files.temp import NamedTemporaryFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.client import Client
from django.test.testcases import TestCase
from django.urls.base import reverse
from scheduler.scheduler import Scheduler
from scheduler.scheduler_impl import OldestFirstScheduler
from utils.basic_entities import FormatEnum
from utils.uncompress_data import CompressedFile
from wiki_quality_web.settings import BASE_DIR, IS_BITBUCKET
from wqual.models.featureset_config import Language, FeatureSet, UsedFeature
from wqual.models.uploaded_datasets import Status
from wqual.models.utils import Format
from wqual.views.featureset_config import ListFeaturesView


class TestDataset(TestCase):
    
    def setUp(self):

        Format.objects.update_enums_in_db()
        Language.objects.update_enums_in_db()
        Status.objects.update_enums_in_db()
        
        self.scheduler = OldestFirstScheduler()
        self.objFormat = Format.objects.get(name=FormatEnum.HTML.name)
        self.language = Language.objects.all()[0]
        self.status = Status.objects.all()[0]
        
        self.password = "meunome"
        self.my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', self.password)
        
        
        
        self.feature_set = FeatureSet.objects.create(nam_feature_set="Featzinho",
                                                     dsc_feature_set="lalalal",
                                                     language=self.language,
                                                     user=self.my_admin)
        dict_feat_per_id = ListFeaturesView.get_features(self.language.name)
        
        #obtain the objects to insert by name
        arrObjFeaturesToInsert = [dict_feat_per_id[nam_feature] for nam_feature in dict_feat_per_id.keys()]
        
        #inser them
        UsedFeature.objects.insert_features_object(self.feature_set,arrObjFeaturesToInsert)
    
    def test_create_remove_dataset(self):
        strDir = BASE_DIR+"/dummy_dataset_tests/"
        strDirResult = BASE_DIR+"/test_results/"
        arqName = "wiki_small.zip" if IS_BITBUCKET else "wiki_big.zip"
        
         
        arrDatasetURLNames = [("extract_features",{}),
                       ("public_extract_features",{"nam_feature_set":self.feature_set.nam_feature_set,"user":self.my_admin.username})]
        intPos = 0
        for dataset_name in arrDatasetURLNames:
            with open(strDir+arqName,"rb") as arq:
                #insere dataset
                c = Client()
                c.login(username=self.my_admin.username, password=self.password)
                
                #faaz requisicao
                str_url = reverse(dataset_name[0],kwargs=dataset_name[1])#
                strArqName = "arquivinho_"+str(intPos)+".zip"
                dataset = SimpleUploadedFile(strArqName, arq.read(), content_type="application/zip")
                response = c.post(str_url, {"feature_set":self.feature_set.id,'format': self.objFormat.id, 'file_dataset': dataset})
                
                #testaa insercao
                lstDataset = self.feature_set.dataset_set.filter(nam_dataset=strArqName)
                
                self.assertEqual(len(lstDataset),1," Could not find the inserted dataset")
                self.assertEqual(response.status_code, 302, "Could not obtain redirect status")
                self.assertEqual(response.url, reverse(dataset_name[0],kwargs=dataset_name[1]), "Did not redirected to the right URL ")
                
                #remove o dataset
                """
                dictDatasetParam = dataset_name[1].copy()
                dictDatasetParam["id_dataset"] = lstDataset[0].id
                strNamURL = "dataset_delete_public" if dataset_name[0]== "public_extract_features" else "dataset_delete"
                str_url = reverse(strNamURL,kwargs=dictDatasetParam)#
                response = c.post(str_url)
                """
                #testa a remoção
                """
                lstDataset = self.feature_set.dataset_set.filter(nam_dataset=strArqName)
                
                self.assertEqual(len(lstDataset),0,"Error in removing dataset")
                self.assertEqual(response.status_code, 302, "Could not obtain redirect status")
                self.assertEqual(response.url, reverse(dataset_name[0],kwargs=dataset_name[1]), "Did not redirected to the right URL ")
                """
                intPos = intPos+1
                #
            """    
            #roda o escalonador
            self.scheduler.run(1, 2)
                
            #obtem o resultado
            c = Client() 
            str_url = reverse("download_result",kwargs=dataset_name[1])
            response = c.post(str_url, {"dataset_id":self.feature_set.dataset_set[0].id,'format': "json"})
            
            f = NamedTemporaryFile("wb",delete=False)
            f.write(response.content)
            f.seek(0)
            
            #Checa se o resultado atual é igual ao resultado já gravado (se o mesmo existir)
            objFileZip = CompressedFile.get_compressed_file(f)
            intFiles = 0
            for name,strFileTxt in objFileZip.read_each_file():
                intFiles = intFiles+1
                self.assertEqual(intFiles, 1, "Deve existir apenas um arquivo")
                resultadoAtual = json.loads(strFileTxt)
                

                
                strArqLastResult = strDirResult+arq+"_result.json"
                if(not os.path.isfile(strArqLastResult)):
                    if(not IS_BITBUCKET):
                        with open(strArqLastResult) as f:
                            print("Arquivo de resultado gravado para outros testes")
                            json.dump(resultadoAtual,f)
                    break
                
                #verifica se o arquivo de resultado atual é igual ao gravado
                with open(strArqLastResult) as f:
                    resultadoOld = json.loads(strFileTxt)
                    
                    mapFeatureOldPerFeatId = resultadoOld["features_description"]
                    mapFeatureAtualPerName = {}
                    for featId,dictData in resultadoAtual["features_description"].items():
                        mapFeatureAtualPerName[dictData["name"]] = featId
                        
                    dataAtual = resultadoAtual["data"]
                    dataOld = resultadoOld["data"]
                    #procura cada arquivo no atual e checa se a feature do old é igual ao feature do atual neste arquivo
                    for arqName,featDictAtual in dataAtual.items():
                        for featId,featVal in dataOld[arqName].items():
                            strFeatName = mapFeatureOldPerFeatId[featId]["name"]
                            featIdAtual = mapFeatureAtualPerName[strFeatName]
                            
                            self.assertEqual(featDictAtual[featIdAtual], featVal, "The feature '"+strFeatName+"' is not the same for the doc '"+arqName+"' ")
                    #caso seja igual, salva outro 
                    if(not IS_BITBUCKET):
                        with open(strArqLastResult) as f:
                            json.dump(resultadoAtual,f)
            """   