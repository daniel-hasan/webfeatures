from feature.features import FeatureDocumentsReader, FeatureDocumentsWriter, FeatureCalculator
from feature.features
from utils.uncompress_data import CompressedFile

import unittest
import json
from CaracterInterface import *



def fun(x):
    return x + 1

class MyTest(unittest.TestCase):
    def test(self):
        self.assertEqual(fun(3), 5)

class TestCaracterInterface(unittest.TestCase):
    def test_le_arquivo(self):
        arrNomeFeature = le_arquivo('arqtest.json')
        self.assertEqual(le_arquivo('arqtest.json'), arrNomeFeature)

if __name__ == "__main__":
    unittest.main()
