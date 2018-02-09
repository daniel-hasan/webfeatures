from feature.feature_factory.feature_factory import WordsFeatureFactory
import unittest
from utils.basic_entities import LanguageEnum, FormatEnum
from feature.featureImpl import WordBasedFeature
import os
from os.path import join, isfile, isdir
from feature.features import Document, FeatureCalculatorManager,\
    FeatureCalculator

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
            

if __name__ == "__main__":
    unittest.main()