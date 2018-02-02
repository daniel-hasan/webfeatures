from feature.feature_factory.feature_factory import WordsFeatureFactory
import unittest
from utils.basic_entities import LanguageEnum
from feature.language_dependent_words.featureImpl import WordBasedFeature

class WordTestFeature(WordBasedFeature):
    '''
    Classe para usar no teste que verifica se o WordBasedFeature está funcionando. 
    '''
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super(WordBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)
        self.arr_str_words = []  
        
          
    def checkWord(self,document,word):
        self.arr_str_words.append(word)
    
    def compute_feature(self,document):
        arr_aux = self.arr_str_words
        self.arr_str_words = []      
        return arr_aux

class TestWordsFeatureFactory(unittest.TestCase):
    
    def test(self):
        
        part_of_speech = ["articles","auxiliaryVerbs","coordinatingConjunctions","correlativeConjunctions",
                          "indefinitePronouns","interrogativePronouns","prepositions","pronouns",
                          "relativePronouns","subordinatingConjunctions","toBeVerbs"]
        
        arr_features = WordsFeatureFactory(LanguageEnum.en)
        arr_features = arr_features.createFeatures()
        
        for feature,classe in arr_features,part_of_speech:
            
            listWords = WordsFeatureFactory.getTestClasseGramatical(classe)
            
            #as listas ao computar a feature tem que ser iguais
            #o compute tem que ler as palavras do documento das classes de palavras, então os dois ficariam iguais
            


if __name__ == "__main__":
    unittest.main()