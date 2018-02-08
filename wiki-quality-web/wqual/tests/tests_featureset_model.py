from django.contrib.auth.models import User
from django.test.testcases import TestCase

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


class FeatureFactoryDummy(FeatureFactory):
    def createFeatures(self):
        
        arrFeatures = [WordCountFeature("Preposition Count","Count the number of prepositions in the text",FeatureVisibilityEnum.public,FormatEnum.text_plain,FeatureTimePerDocumentEnum.MICROSECONDS,setWordsToCount=["de","do","du"])]
        featLargeSentenceCount = LargeSentenceCountFeature("Largest Phrase Count","Count the number of phrases larger than a specified threshold",FeatureVisibilityEnum.public,FormatEnum.text_plain,FeatureTimePerDocumentEnum.MICROSECONDS,10)
        featLargeSentenceCount.addConfigurableParam(ConfigurableParam("int_sentence_size","Sentence Size",
                                                                      "The sentence need to have (at least) this length (in words) in order to be considered a large phrase",
                                                                10,ParamTypeEnum.int))
        arrFeatures.append(featLargeSentenceCount)
        return arrFeatures
class FeatureFactoryDummyLangDep(FeatureFactory):
    def __init__(self,objLanguage):
        self.objLanguage = objLanguage
    def createFeatures(self):
        
        arrFeatures = [WordCountFeature("Preposition Count "+self.objLanguage.name,"Count the number of prepositions in the text",FeatureVisibilityEnum.public,FormatEnum.text_plain,FeatureTimePerDocumentEnum.MICROSECONDS,setWordsToCount=["de","do","du"])]
        featLargeSentenceCount = LargeSentenceCountFeature("Largest Phrase Count "+self.objLanguage.name,"Count the number of phrases larger than a specified threshold",FeatureVisibilityEnum.public,FormatEnum.text_plain,FeatureTimePerDocumentEnum.MICROSECONDS,10)
        featLargeSentenceCount.addConfigurableParam(ConfigurableParam("int_sentence_size","Sentence Size",
                                                                      "The sentence need to have (at least) this length (in words) in order to be considered a large phrase",
                                                                10,ParamTypeEnum.int))
        arrFeatures.append(featLargeSentenceCount)
        return arrFeatures
class TestUsedFeatures(TestCase):
    def setUp(self):

        Format.objects.update_enums_in_db()
        Language.objects.update_enums_in_db()
        Status.objects.update_enums_in_db()
        
        self.objFormat = Format.objects.all()[0]
        self.language = Language.objects.all()[0]
        self.status = Status.objects.all()[0]
        
        self.password = "meunome"
        self.my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', self.password)
        self.feature_set = FeatureSet.objects.create(group="g1",nam_feature_set="Featzinho",
                                                     dsc_feature_set="lalalal",
                                                     language=self.language,
                                                     user=self.my_admin)
        FeatureFactoryBD.objects.create(nam_module="wqual.tests.tests_featureset_model",
                                      nam_class="FeatureFactoryDummy")
        FeatureFactoryBD.objects.create(nam_module="wqual.tests.tests_featureset_model",
                                      nam_class="FeatureFactoryDummyLangDep")
    def test_feature_list(self):
        objEnglish = Language.objects.get(name="en")
        arrFeatures = FeatureFactoryBD.objects.get_all_features_from_language(objEnglish)
        
        #get features names
        arrFeatureNames = [objFeature.name for objFeature in arrFeatures]
        #sort
        arrExpected = ["Largest Phrase Count","Largest Phrase Count "+objEnglish.name,"Preposition Count","Preposition Count "+objEnglish.name]
        
        self.assertListEqual(arrFeatureNames, arrExpected)
        
    def _assertFeatureEqual(self,objFeatureBD,objFeatureObjPython):
        self.assertEqual(objFeatureBD.visibility.get_enum(), objFeatureObjPython.visibility, "The visibility attr is not equal")
        self.assertEqual(objFeatureBD.text_format.get_enum(), objFeatureObjPython.text_format, "The text_format attr is not equal")
        self.assertEqual(objFeatureBD.feature_time_per_document.get_enum(), objFeatureObjPython.feature_time_per_document, "The feature_time_per_document attr is not equal")
        
        
        #atts: name, description, reference and arr_config_feautre
        for argVal in objFeatureBD.usedfeatureargs_set.all():
            if(argVal.nam_argument=="name"):
                self.assertEqual(argVal.val_argument, objFeatureObjPython.name, "The "+argVal.nam_argument+" attr is not equal")
                
            elif(argVal.nam_argument=="description"):
                self.assertEqual(argVal.val_argument, objFeatureObjPython.description, "The "+argVal.nam_argument+" attr is not equal")
            
            elif(argVal.nam_argument=="reference"):
                self.assertEqual(argVal.val_argument, objFeatureObjPython.reference, "The "+argVal.nam_argument+" attr is not equal")
            else
                #if is a configurable param, search in objFeatureObjPython.arr_configurable_param otherwise, seach in the feaatures attrs
                if(argVal.is_configurable):
                    for(confParam in objFeatureObjPython.arr_configurable_param):
                        pass
                else:
                    for(attrKeyObjPython,attrValObjPython in objFeatureObjPython.__dict__.items()):
                        if(attrKeyObjPython == argVal.nam_argument):
                            pass
                            

    
    def test_feature_add(self):
        wordCount = WordCountFeature("Preposition Count","Count the number of prepositions in the text",FeatureVisibilityEnum.public,FormatEnum.text_plain,FeatureTimePerDocumentEnum.MICROSECONDS,setWordsToCount=["de","do","du"])
        featLargeSentenceCount = LargeSentenceCountFeature("Largest Phrase Count","Count the number of phrases larger than a specified threshold",FeatureVisibilityEnum.public,FormatEnum.text_plain,FeatureTimePerDocumentEnum.MICROSECONDS,10)
        featLargeSentenceCount.addConfigurableParam(ConfigurableParam("int_sentence_size","Sentence Size",
                                                                      "The sentence need to have (at least) this length (in words) in order to be considered a large phrase",
                                                                22,ParamTypeEnum.int))
        
        featLargeSentenceCount.addConfigurableParam(ConfigurableParam("str_name","Name",
                                                                      "The sentence need to have (at least) this length (in words) in order to be considered a large phrase",
                                                                "oioi",ParamTypeEnum.string))
        
        arrObjectFeatures = [wordCount,featLargeSentenceCount]
        UsedFeature.objects.insert_features_object(self.featureSet, arrObjectFeatures)
        
        #pega todos os used features 
        arrUsedFeatures = UsedFeature.objects.filter(id=self.featureSet.pk)
        self.assertEqual(len(arrUsedFeatures), 2, "Deveria ter 2 features e tem "+len(arrUsedFeatures))
        for objFeatureUsed in arrUsedFeatures:
            msg="The feature should be Preposition Count or Largest Phrase Count but it was "+objFeatureUsed.name
            self.assertTrue(objFeatureUsed.name == "Preposition Count" or objFeatureUsed.name == "Largest Phrase Count", msg)
            if(objFeatureUsed.name == "Preposition Count"):
                self._assertFeatureEqual(objFeatureUsed,wordCount)
            elif(objFeatureUsed.name == "Largest Phrase Count"):
                self._assertFeatureEqual(objFeatureUsed,wordCount)
        
        
        
    def test_view_feature_list_add(self):
        pass 
    