'''
Created on 28 de jun de 2018

@author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
Views relacionadas a criação do dataset
'''
import json
import os.path
import csv

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
from wqual.models.uploaded_datasets import Status, StatusEnum
from wqual.models.utils import Format
from wqual.views.featureset_config import ListFeaturesView
from feature.featureImpl.readability_features import ReadabilityBasedFeature


CHECK_IF_FEAT_NOT_EXISTS = True

def JSONToDict(strTxt):
        return json.loads(strTxt)
def CSVToDict(strTxt):
    csv_list = csv.reader(strTxt.split("\n"))
    dictJSON = {"features_description":{},
                "data":{}}
    bolFirstLine = True 
    #primeira linha contem o nome das features
    for linha in csv_list: 
        if(bolFirstLine):      
            for i,col in enumerate(linha[1:]):
                dictJSON["features_description"][str(i)] = {"name":col}
            bolFirstLine = False
        else: 
            #dados por linha: primeiro coluna éo nome do arquivo e as demais são os valores das features
            if(len(linha)>0):
                strFileName = linha[0]
                dictJSON["data"][strFileName] = {}
                for i,colFeat in enumerate(linha[1:]):
                    dictJSON["data"][strFileName][str(i)] = colFeat
        
    return dictJSON
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
        arrNames = dict_feat_per_id.keys()
        #Para ler a ordem de arquivo (Caso a ordem tenha dado algum erro)
        #with open("/home/profhasan/saida.json","r") as f:
        #    arrNames = json.load(f)
        arrObjFeaturesToInsert = [dict_feat_per_id[nam_feature] for nam_feature in arrNames] #if isinstance(dict_feat_per_id[nam_feature], ReadabilityBasedFeature)]
        #Imprime features
        #[print("Feat:"+feat.name) for feat in arrObjFeaturesToInsert]
        
        #grava as features usadas na ordem 
        arrFeats = []
        for i,feat in enumerate(arrObjFeaturesToInsert):
            arrFeats.append(feat.name)
        if(not IS_BITBUCKET):
            with open("~/saida.json","w") as fp:
                json.dump(arrFeats, fp)
            
        #inser them
        UsedFeature.objects.insert_features_object(self.feature_set,arrObjFeaturesToInsert)
    def insert_dataset_test(self,client,arq,dataset_name,intPos):
        #faaz requisicao
        str_url = reverse(dataset_name[0],kwargs=dataset_name[1])#
        strArqName = "arquivinho_"+str(intPos)+".zip"
        dataset = SimpleUploadedFile(strArqName, arq.read(), content_type="application/zip")
        response = client.post(str_url, {"feature_set":self.feature_set.id,'format': self.objFormat.id, 'file_dataset': dataset})
                
        #testaa insercao
        lstDataset = self.feature_set.dataset_set.filter(nam_dataset=strArqName)
                
        self.assertEqual(len(lstDataset),1," Could not find the inserted dataset")
        self.assertEqual(response.status_code, 302, "Could not obtain redirect status")
        self.assertEqual(response.url, reverse(dataset_name[0],kwargs=dataset_name[1]), "Did not redirected to the right URL ")
        
        return lstDataset[0]
    def remove_dataset_test(self,dataset_name,client,objDataset):
        #remove o dataset
        dictDatasetParam = dataset_name[1].copy()
        dictDatasetParam["id_dataset"] = objDataset.id
        strDatasetFileName = objDataset.nam_dataset
        strNamURL = "dataset_delete_public" if dataset_name[0]== "public_extract_features" else "dataset_delete"
        str_url = reverse(strNamURL,kwargs=dictDatasetParam)#
        response = client.post(str_url)
        
        #testa a remoão
        self.feature_set.refresh_from_db()
        lstDataset = self.feature_set.dataset_set.filter(nam_dataset=strDatasetFileName)

        self.assertEqual(response.status_code, 302, "Could not obtain redirect status: url:"+str_url+" response: "+str(response))
        self.assertEqual(response.url, reverse(dataset_name[0],kwargs=dataset_name[1]), "Did not redirected to the right URL ")        
        self.assertEqual(len(lstDataset),0,"Error in removing dataset")

    
        
    def get_resultado_atual(self,response,funcToConvert):
        
        f = NamedTemporaryFile("wb",delete=False)
        #print(str(response))
        f.write(response.content)
        f.close()
        with open(f.name,"rb") as f:
            objFileZip = CompressedFile.get_compressed_file(f)
            intFiles = 0
            resultadoAtual = None
            for name,strFileTxt in objFileZip.read_each_file():
                intFiles = intFiles+1
                self.assertEqual(intFiles, 1, "Deveria existir apenas um arquivo")
                #print(strFileTxt.decode("utf-8"))
                resultadoAtual = funcToConvert(strFileTxt.decode("utf-8"))
            self.assertNotEqual(resultadoAtual,None,"Deveria existir um resultado atual")
            return resultadoAtual
    def grava_last_result(self,strArqLastResult,resultado):
        if(not IS_BITBUCKET):
            with open(strArqLastResult,"w") as f:
                json.dump(resultado,f)
                return True
        return False
    def dictDifsToStr(self,dicDifs):
        strFeatureNames = ",".join(dicDifs.keys())
        
        return "The features: "+strFeatureNames+" contain different results in the following documents: \n"+str(dicDifs)
    def compare_result(self,resultadoOld,resultadoAtual):
        mapFeatureOldPerFeatId = resultadoOld["features_description"]
        mapFeatureAtualPerName = {}
        for featId,dictData in resultadoAtual["features_description"].items():
            mapFeatureAtualPerName[dictData["name"]] = featId
        dataAtual = resultadoAtual["data"]
        dataOld = resultadoOld["data"]
            
        #procura cada arquivo no atual e checa se a feature do old é igual ao feature do atual neste arquivo
        dictDifs = {}
        for arqName,featDictAtual in dataAtual.items():
            for featId,featVal in dataOld[arqName].items():
                strFeatName = mapFeatureOldPerFeatId[featId]["name"]
                
                if(CHECK_IF_FEAT_NOT_EXISTS):
                    self.assertTrue(strFeatName in mapFeatureAtualPerName, "Could not found the feature '"+strFeatName+"' in the current FeatureSet")
                if(strFeatName in mapFeatureAtualPerName):
                    featIdAtual = mapFeatureAtualPerName[strFeatName]
                    if(str(featDictAtual[featIdAtual]) != str(featVal)):
                        if strFeatName not in dictDifs:
                            dictDifs[strFeatName] = []
                        dictDifs[strFeatName].append((arqName,featVal,featDictAtual[featIdAtual]))
        self.assertEqual(len(dictDifs.keys()), 0, self.dictDifsToStr(dictDifs))        
    def compare_old_result(self,strArqLastResult,resultadoAtual):
        with open(strArqLastResult) as f:
            resultadoOld = json.load(f)
            #print("----------- Resultado atual: -----------------")
            #print(str(resultadoAtual["data"]['10308286.html']))
            #print("----------- Resultado old: -----------------")
            #print(str(resultadoOld["data"]['10308286.html']))
            self.compare_result(resultadoOld, resultadoAtual)
                    

                     
        if(not IS_BITBUCKET):
            self.grava_last_result(strArqLastResult, resultadoAtual)
    
    
    def request_resultados(self,client,formatResult):
        paramResult = {}
        paramResult["dataset_id"] = self.feature_set.dataset_set.all()[0].id
        paramResult["format"] = formatResult
        

            
        str_url = reverse("download_result",kwargs=paramResult)
        response = client.get(str_url)
        self.assertEqual(response.status_code, 200, "Could not obtain sucess status")
        return response
    
    def test_create_remove_dataset(self):
        SUBMITTED_STATUS = Status.objects.get(name=StatusEnum.SUBMITTED.name)
        COMPLETE_STATUS = Status.objects.get(name=StatusEnum.COMPLETE.name)
        
        strDir = BASE_DIR+"/dummy_dataset_tests/"
        strDirResult = BASE_DIR+"/test_results/"
        arqName = "wiki_small.zip" #if IS_BITBUCKET else "wiki_big.zip"
        #arqName = "wiki_big.zip"
         
        arrDatasetURLNames = [("extract_features",{}),
                       ("public_extract_features",{"nam_feature_set":self.feature_set.nam_feature_set,"user":self.my_admin.username})]
        intPos = 0
        for dataset_name in arrDatasetURLNames:
            c = Client()
            c.login(username=self.my_admin.username, password=self.password)
            
            objDataset = None
            with open(strDir+arqName,"rb") as arq:
                
                objDataset = self.insert_dataset_test(c, arq, dataset_name, intPos)
                
                #

                
                #
            
            #roda o escalonador e testa
            self.assertEqual(objDataset.status.name, SUBMITTED_STATUS.name, "Wrong status. It should be submitted.")
            if(intPos == 0):
                self.scheduler.run(1, 3)
                objDataset.refresh_from_db()
                self.assertEqual(objDataset.status.name, COMPLETE_STATUS.name, "Wrong status. It should be completed.")
                
                
                #obtem o resultado
                strArqLastResult = strDirResult+arqName+"_result.json"
                responseJSON = self.request_resultados(c,"json")
                
                #Checa se o resultado atual é igual ao resultado já gravado (se o mesmo existir)            #
                resultadoAtual = self.get_resultado_atual(responseJSON,JSONToDict)
                
                #grava como ultimo resultado - se o mesmo nao exitir
                if(not os.path.isfile(strArqLastResult)):
                    self.grava_last_result(strArqLastResult,resultadoAtual)
                    print("ARquivo resultado gravado: "+strArqLastResult)
                else:
                    #se existir, verifica se o arquivo de resultado atual é igual ao gravado
                    print("Verificando se é igual...")
                    self.compare_old_result(strArqLastResult, resultadoAtual)
                
                #compara o xls com o json
                responseCSV = self.request_resultados(c,"csv")
                resultadoCSV = self.get_resultado_atual(responseCSV,CSVToDict)
                self.compare_result(resultadoCSV, resultadoAtual)
                self.compare_result(resultadoAtual, resultadoCSV)
            
            #remove o dataset
            self.remove_dataset_test(dataset_name, c, objDataset)
            intPos = intPos+1