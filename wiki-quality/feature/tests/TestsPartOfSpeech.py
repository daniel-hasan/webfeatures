from feature.feature_factory.feature_factory import WordsFeatureFactory
import unittest

from utils.basic_entities import LanguageEnum

class TestFile(unittest.TestCase):
    
    def test(self):
        
        classe = WordsFeatureFactory(LanguageEnum.en)
        for word in classe.getTestClasseGramatical("prepositions"):
            print(str(word).title() + "\n")

if __name__ == "__main__":
    unittest.main()
    
    