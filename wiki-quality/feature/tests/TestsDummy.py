'''
Created on 4 de set de 2017
Testes de todas as classes abstratas de calculo das features
@author: Daniel Hasan Dalip hasan@decom.cefetmg.br
'''
import unittest


class TestFeatureCalculator(unittest.TestCase):

    def testLALLA(self):
        self.assertEqual(0, 0)
        
    def testErro(self):
        self.assertEqual(0, 1,"Deu erro!")
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'TestFeatureCalculator.testName']
    unittest.main()