import json
#from feature.features import FeatureDocumentsReader, FeatureDocumentsWriter, FeatureCalculator
#from feature.features import
#from utils.uncompress_data import CompressedFile

import unittest
import CaracterInterface #importamos



def fun(x):
    return x + 1

class MyTest(unittest.TestCase):
    def test(self):
        self.assertEqual(fun(3), 5)
