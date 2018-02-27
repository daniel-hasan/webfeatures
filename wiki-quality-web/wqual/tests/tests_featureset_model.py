from django.contrib.auth.models import User
from django.test.client import Client
from django.test.testcases import TestCase
from django.urls.base import reverse
import inspect
import json

from feature.featureImpl.style_features import WordCountFeature, \
    LargeSentenceCountFeature
from feature.feature_factory.feature_factory import FeatureFactory
from feature.features import FeatureVisibilityEnum, ConfigurableParam, \
    ParamTypeEnum
from utils.basic_entities import FormatEnum, FeatureTimePerDocumentEnum
from wqual.models.featureset_config import Language, FeatureSet, FeatureFactory as FeatureFactoryBD, \
    UsedFeature
from wqual.models.uploaded_datasets import Status
from wqual.models.utils import Format
from wqual.views.featureset_config import ListFeaturesView


class FeatureFactoryDummy(FeatureFactory):
    def createFeatures(self):
        
        arrFeatures = [WordCountFeature("Preposition Count","Count the number of prepositions in the text","ref",FeatureVisibilityEnum.public,FormatEnum.text_plain,FeatureTimePerDocumentEnum.MICROSECONDS,setWordsToCount=["de","do","du"])]
        featLargeSentenceCount = LargeSentenceCountFeature("Largest Phrase Count","Count the number of phrases larger than a specified threshold","ref",FeatureVisibilityEnum.public,FormatEnum.text_plain,FeatureTimePerDocumentEnum.MICROSECONDS,10)
        featLargeSentenceCount.addConfigurableParam(ConfigurableParam("int_size","Sentence Size",
                                                                      "The sentence need to have (at least) this length (in words) in order to be considered a large phrase",
                                                                10,ParamTypeEnum.int))
        arrFeatures.append(featLargeSentenceCount)
        
        return arrFeatures
class FeatureFactoryDummyLangDep(FeatureFactory):
    IS_LANGUAGE_DEPENDENT = True
    
    def __init__(self,objLanguage):
        self.objLanguage = objLanguage
    def createFeatures(self):
        
        arrFeatures = [WordCountFeature("Preposition Count "+self.objLanguage.name,"Count the number of prepositions in the text","ref",FeatureVisibilityEnum.public,FormatEnum.text_plain,FeatureTimePerDocumentEnum.MICROSECONDS,setWordsToCount=["de","do","du"])]
        featLargeSentenceCount = LargeSentenceCountFeature("Largest Phrase Count "+self.objLanguage.name,"Count the number of phrases larger than a specified threshold","ref",FeatureVisibilityEnum.public,FormatEnum.text_plain,FeatureTimePerDocumentEnum.MICROSECONDS,10)
        featLargeSentenceCount.addConfigurableParam(ConfigurableParam("int_size","Sentence Size",
                                                                      "The sentence need to have (at least) this length (in words) in order to be considered a large phrase",
                                                                10,ParamTypeEnum.int))
        arrFeatures.append(featLargeSentenceCount)
        return arrFeatures
class TestUsedFeatures(TestCase):
    STR_FEAT_NAME1 = "__PrepCount OI__"
    STR_FEAT_NAME2 = "__LargeFeat OI__"
    
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
        FeatureFactoryBD.objects.create(nam_module="wqual.tests.tests_featureset_model",
                                      nam_factory_class="FeatureFactoryDummy")
        FeatureFactoryBD.objects.create(nam_module="wqual.tests.tests_featureset_model",
                                      nam_factory_class="FeatureFactoryDummyLangDep")

        
    def assertFeatureEqual(self,objFeatureBD,objFeatureObjPython):
        #verifica atributos (visibility,format, time se sao iguais)
        self.assertEqual(objFeatureBD.feature_visibility.get_enum(), objFeatureObjPython.visibility, "The visibility attr is not equal")
        self.assertEqual(objFeatureBD.text_format.get_enum(), objFeatureObjPython.text_format, "The text_format attr is not equal")
        self.assertEqual(objFeatureBD.feature_time_to_extract.get_enum(), objFeatureObjPython.feature_time_per_document, "The feature_time_per_document attr is not equal")
        
        #obtem os parametros no construtor para verificar se sao os mesmos
        arrParamsConstrutor = set(inspect.getargspec(objFeatureObjPython.__init__).args[1:])
        
        #search if the att in bd were in objFeatureObjPython
        set_configurable_params_bd = set([])
        for argVal in objFeatureBD.usedfeatureargval_set.all():
            if(argVal.nam_argument=="name"):
                self.assertEqual(argVal.val_argument, objFeatureObjPython.name, "The "+argVal.nam_argument+" attr is not equal")
                
            elif(argVal.nam_argument=="description"):
                self.assertEqual(argVal.val_argument, objFeatureObjPython.description, "The "+argVal.nam_argument+" attr is not equal")
            
            elif(argVal.nam_argument=="reference"):
                self.assertEqual(argVal.val_argument, objFeatureObjPython.reference, "The "+argVal.nam_argument+" attr is not equal")
            else:
                
                #if is a configurable param, search in objFeatureObjPython.arr_configurable_param    
                if(argVal.is_configurable):
                    set_configurable_params_bd.add(argVal.nam_argument)
                    bolEncontrou = False
                    for confParam in objFeatureObjPython.arr_configurable_param:
                        if(confParam.att_name == argVal.nam_argument):
                            bolEncontrou = True
                            self.assertEqual(argVal.val_argument, str(UsedFeature.objects.from_obj_to_bd_type_val(confParam.default_value)[1]), "The "+argVal.nam_argument+" attr was not set to default")
                    self.assertTrue(bolEncontrou, "Could not find the configurable parameter: "+argVal.nam_argument+" in the feature object")
                    
                #search the att in att args
                for namAtt in arrParamsConstrutor:
                    valAtt = objFeatureObjPython.__dict__[namAtt]
                    if(namAtt == argVal.nam_argument):
                            bolEncontrou = True
                            if(not argVal.is_configurable):
                                self.assertEqual(argVal.val_argument, str(UsedFeature.objects.from_obj_to_bd_type_val(valAtt)[1]), "The "+argVal.nam_argument+" attr was not igual in the object")
                            self.assertTrue(bolEncontrou, "Could not find the parameter: "+argVal.nam_argument+" in the feature object")
        #search if all the construtor atts are in BD (expept visibility,text_format and feature_time_per_document)
        for strConstructorParam in arrParamsConstrutor:
            if(strConstructorParam not in ("visibility","text_format","feature_time_per_document")):
                bolEncontrou = False
                for argVal in objFeatureBD.usedfeatureargval_set.all():
                    if(argVal.nam_argument == strConstructorParam):
                        bolEncontrou = True
                self.assertTrue(bolEncontrou, "Could not find the parameter: "+argVal.nam_argument+" in the database")
        set_configurable_params =set([confParam.att_name for confParam in objFeatureObjPython.arr_configurable_param])
        self.assertSetEqual(set_configurable_params_bd, set_configurable_params, "The set of configurable params in BD and in the object are diferent in the feature '"+objFeatureObjPython.name+"'")
        #print("Set in BD:"+str(set_configurable_params_bd)+" set in obj: "+str(set_configurable_params))
                
    def test_feature_list(self):
        objEnglish = Language.objects.get(name="en")
        arrFeatures = FeatureFactoryBD.objects.get_all_features_from_language(objEnglish)
        
        #get features names
        arrFeatureNames = [objFeature.name for objFeature in arrFeatures]
        arrFeatureNames.sort()
        
        #sort
        arrExpected = ["Largest Phrase Count","Largest Phrase Count "+objEnglish.name,"Preposition Count","Preposition Count "+objEnglish.name]
        for str_expected_feature_name in arrExpected:
            bolEncontrou = False
            for feature in arrFeatures:
                if(str_expected_feature_name == feature.name):
                    bolEncontrou = True
            self.assertTrue(bolEncontrou, "Could not found the feature: "+str_expected_feature_name)
            
    
    def test_feature_add(self):
        wordCount = WordCountFeature("Preposition Count","Count the number of prepositions in the text","ref",FeatureVisibilityEnum.public,FormatEnum.text_plain,FeatureTimePerDocumentEnum.MICROSECONDS,setWordsToCount=["de","do","du"])
        featLargeSentenceCount = LargeSentenceCountFeature("Largest Phrase Count","Count the number of phrases larger than a specified threshold","ref",FeatureVisibilityEnum.public,FormatEnum.text_plain,FeatureTimePerDocumentEnum.MICROSECONDS,10)
        featLargeSentenceCount.addConfigurableParam(ConfigurableParam("int_size","Sentence Size",
                                                                      "The sentence need to have (at least) this length (in words) in order to be considered a large phrase",
                                                                22,ParamTypeEnum.int))
        
        #featLargeSentenceCount.addConfigurableParam(ConfigurableParam("str_name","Name",
        #                                                              "The sentence need to have (at least) this length (in words) in order to be considered a large phrase",
        #                                                        "oioi",ParamTypeEnum.string))
        
        arrObjectFeatures = [wordCount,featLargeSentenceCount]
        UsedFeature.objects.insert_features_object(self.feature_set, arrObjectFeatures)
        
        #pega todos os used features 
        arrUsedFeatures = UsedFeature.objects.filter(feature_set=self.feature_set.pk)
        self.assertEqual(len(arrUsedFeatures), 2, "Deveria ter 2 features e tem "+str(len(arrUsedFeatures)))
        for objFeatureUsed in arrUsedFeatures:
            str_nameFeature = objFeatureUsed.usedfeatureargval_set.get(nam_argument="name").val_argument
                
            msg="The feature should be Preposition Count or Largest Phrase Count but it was "+str_nameFeature
            self.assertTrue(str_nameFeature == "Preposition Count" or str_nameFeature == "Largest Phrase Count", msg)
            if(str_nameFeature == "Preposition Count"):
                self.assertFeatureEqual(objFeatureUsed,wordCount)
            elif(str_nameFeature == "Largest Phrase Count"):
                self.assertFeatureEqual(objFeatureUsed,featLargeSentenceCount)
        
        
    
    def test_view_feature_list(self,language_code="en"):
        c = Client()
        c.login(username=self.my_admin.username, password=self.password)
        
        #list all the features correctly
        str_url = reverse("list_all_features",kwargs={"nam_language":language_code})
        response = c.post(str_url, {})
        self.assertEqual(response.status_code, 200, "could not obtain a status 200")
        
        #check if found the feature names
        arrFeatNames = ["Largest Phrase Count","Largest Phrase Count "+language_code,"Preposition Count","Preposition Count "+language_code]
        
        arrFeatures = response.json()['arrFeatures']
        
        for str_expected_feature_name in arrFeatNames:
            bolEncontrou = False
            for feature in arrFeatures:
                if(str_expected_feature_name == feature['name']):
                    bolEncontrou = True
            self.assertTrue(bolEncontrou, "Could not found the feature: "+str_expected_feature_name)
        
        return arrFeatures
    def assert_feature_add(self,client,str_url,arrFeatNames,arr_num_of_config_args):
        
        strPostFeatNames = json.dumps(arrFeatNames)
        response = client.post(str_url, {"hidUsedFeaturesToInsert":strPostFeatNames})
        self.assertEqual(response.status_code, 200, "could not obtain a status 200")
    
        #check if found the feature names
        arrUsedFeatures = response.json()['arrUsedFeatures']
        intI = 0
        for str_expected_feature_name in arrFeatNames:
            bolEncontrou = False
            for feature in arrUsedFeatures:
                if(str_expected_feature_name == feature['name']):
                    self.assertTrue(feature['used_feature_id'] != None, "Used feature cannot be None")
                    bolEncontrou = True
                    
                    #test the feature param 
                    arrParam = feature['arr_param']
                    self.assertEqual(len(arrParam), arr_num_of_config_args[intI], "The number of configured param for the feature '"+feature['name']+"' is not the same. Expected: "+str(arr_num_of_config_args[intI]))
                    if(len(arrParam)>0):
                        self.assertTrue(feature['is_configurable'], "The number of params is greater than zero, then, the is_configurable must be true")
                    else:
                        self.assertTrue(not feature['is_configurable'], "The number of params is zero, then, the is_configurable must be false")
                    intI = intI+1
                    
            self.assertTrue(bolEncontrou, "Could not found the feature: "+str_expected_feature_name)
            
                
    def test_view_feature_add(self):
        c = Client()
        c.login(username=self.my_admin.username, password=self.password)
        
        #list all the features correctly
        str_url = reverse("insert_used_features",kwargs={"nam_feature_set":self.feature_set.nam_feature_set})
        objLanguage = self.feature_set.language
        
        #test inserting 2 features
        arrFeatNames = ["Largest Phrase Count "+objLanguage.name,"Preposition Count"]
        self.assert_feature_add(c,str_url,arrFeatNames,[1,0])
        
        #test inserting all the features
        objFeatureSet = FeatureSet.objects.create(nam_feature_set="Featzinho2",
                                                     dsc_feature_set="lalalal",
                                                     language=self.language,
                                                     user=self.my_admin)
        #get all the features
        dict_feat_per_id = ListFeaturesView.get_features(self.language.name)
        #prepare the array of features    
        arrParamPerFeature = []
        arrFeatNames=[]
        for name,objFeature in dict_feat_per_id.items():
            arrFeatNames.append(name)
            arrParamPerFeature.append(len(objFeature.arr_configurable_param))
        print("Number of feats: "+str(len(arrFeatNames)))
        print("Feat names: "+str(arrFeatNames))
        
        
        str_url = reverse("insert_used_features",kwargs={"nam_feature_set":objFeatureSet.nam_feature_set})
        self.assert_feature_add(c,str_url,arrFeatNames,arrParamPerFeature)
            
        
        
        
        