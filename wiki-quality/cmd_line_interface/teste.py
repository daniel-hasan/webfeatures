#from feature.features import FeatureDocumentsReader, FeatureDocumentsWriter, FeatureCalculator
#from feature.features
#from utils.uncompress_data import CompressedFile

import unittest
import json
from .CaracterInterface import *



def fun(x):
    return x + 1

class MyTest(unittest.TestCase):
    def test(self):
        self.assertEqual(fun(3), 5)
