import json
#from feature.features import FeatureDocumentsReader, FeatureDocumentsWriter, FeatureCalculator
#from feature.features import
#from utils.uncompress_data import CompressedFile

import unittest
from .CaracterInterface import * #importamos



def fun(x):
    return x + 1

class MyTest(unittest.TestCase):
    def test(self):
        self.assertEqual(fun(4), 5)
        

#teste
class TestCaracterInterface(unittest.TestCase):
    def testObtemObjetosFeatures(self):
        
        novoCaracterInterface = CaracterInterface()
        
        arrNomesFeatures = ["Section count","Subsection count","Complete URL link count"]
        
        arr_obj_features = novoCaracterInterface.obtemObjetosFeatures(arrNomesFeatures)
        
        self.assertEqual(len(arrNomesFeatures),len(arr_obj_features), "Erro! A lista de objetos de features não saiu como o esperado")

        ok = False
        for feat,nome in zip(arr_obj_features,arrNomesFeatures):
            ok=True
            self.assertEqual(feat.name,nome,"Erro! Nomes apresentam divergência")
           
        self.assertTrue(ok,"Certifique-se que as listas não estejam vazias!")
        
        
if __name__ == "__main__":
    unittest.main()
                
        
        
