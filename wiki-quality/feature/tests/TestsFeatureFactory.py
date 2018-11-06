import os
from os.path import join, isfile, isdir
import unittest

from feature.featureImpl import WordBasedFeature
from feature.feature_factory.feature_factory import WordsFeatureFactory, \
    FeatureFactory
from feature.features import Document, FeatureCalculatorManager, \
    FeatureCalculator
from utils.basic_entities import LanguageEnum, FormatEnum, CheckTime


class TestWordsFeatureFactory(unittest.TestCase):
    
    def test(self):
        
        BASE_DIR = os.path.abspath(__file__)
        BASE_DIR = os.path.abspath(os.path.join(BASE_DIR,os.pardir))
        dir_file = BASE_DIR + "/docTests/partofspeech.txt"
        
        with open(dir_file) as file:
            str_text = file.read()
        
        doc = Document(1,"doc1",str_text)        
        part_of_speech = ["articles","auxiliaryVerbs","coordinatingConjunctions","correlativeConjunctions",
                          "indefinitePronouns","interrogativePronouns","prepositions","pronouns",
                          "relativePronouns","subordinatingConjunctions","toBeVerbs"]
        
        objFeatFactory = WordsFeatureFactory(LanguageEnum.en)
        
        for classe in part_of_speech:
            arr_features = [objFeatFactory.createFeatureObject(classe)]
            objFeatureCalculator = FeatureCalculatorManager()
            arr_feature_result = objFeatureCalculator.computeFeatureSet(doc, arr_features, FormatEnum.text_plain)
            self.assertEqual(2, arr_feature_result[0], classe + " não foi computado corretamente\n")
    
    def tests_all_features(self):
        print("===========================================================")
        BASE_DIR = os.path.abspath(__file__)
        BASE_DIR = os.path.abspath(os.path.join(BASE_DIR,os.pardir))
        dir_file = BASE_DIR + "/docTests/222902.html"
        timeToProc = CheckTime()
        #peogu o texto
        with open(dir_file) as file:
            str_text = file.read()
        doc = Document(1,"doc1",str_text)      
        timeToProc.printDelta("Leitura do arquivo")
        #gerar todas ass features
        objEnglish = LanguageEnum.en
        
        arrFeatures = []
        for SubClass in FeatureFactory.subclasses__():
            objFeatFact = None
            if(SubClass.IS_LANGUAGE_DEPENDENT):
                objFeatFact = SubClass(objEnglish)
            else:
                objFeatFact = SubClass()
            
            [arrFeatures.append(feat) for feat in objFeatFact.createFeatures()]
        timeToProc.printDelta("Pega as features")
        #roda o manager    
        objFeatureCalculator = FeatureCalculatorManager()
        arr_feature_result = objFeatureCalculator.computeFeatureSet(doc, arrFeatures, FormatEnum.HTML)
        
                
                

if __name__ == "__main__":
    unittest.main()