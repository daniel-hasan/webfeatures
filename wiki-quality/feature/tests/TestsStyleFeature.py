'''
Created on 4 de set de 2017
Testes de todas as classes abstratas de calculo das features
@author: Daniel Hasan Dalip hasan@decom.cefetmg.br
'''
import unittest
from feature.featureImpl.style_features import WordCountFeature
from feature.features import FeatureVisibilityEnum, Document
from utils.basic_entities import FormatEnum, FeatureTimePerDocumentEnum


class TestFeatureCalculator(unittest.TestCase):
    

    def setUp(self):
        '''
            Implemente esse método para criar algo antes do teste
        '''
        pass


    def tearDown(self):
        '''
            Implemente esse método para eliminar algo feito no teste
        '''
        pass
        
    def testWordCountTest(self):
        '''
            Rode a  WordCountFeature chamando o "checkword" e, logo apos, o featureResult para algumas palavras (alguams que pertençam 
            a lista que você criou e algumas que não pertencem a lista.
            @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>  
        '''
        wcount = WordCountFeature("ola feature contadora", "Essa feature é divertitida", 
                                         "SILVA Ola. Contando Olas. Conferencia dos Hello World", 
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.text_plain, 
                                         FeatureTimePerDocumentEnum.MILLISECONDS,["de","do"],
                                         case_sensitive=True)
        
        document = Document(1,"doc1","O texto nao precisa -necessariamente - ser o texto que sera testado")
        
        #teste quando há verias palavras
        wcount.checkWord(document, "oi")
        wcount.checkWord(document, ",")
        wcount.checkWord(document, " ")
        wcount.checkWord(document, "de")
        wcount.checkWord(document, "de")
        wcount.checkWord(document, "é")
        wcount.checkWord(document, "do")
        int_result = wcount.compute_feature(document)
        self.assertEqual(int_result, 3, "Nao foi contabilizado o numero de palavras corretos no teste do primeiro documento")
        
        #teste quando o texto não possul palavra alguma
        int_result = wcount.compute_feature(document)
        self.assertEqual(int_result, 0, "Nao foi contabilizado o numero de palavras corretos no teste do segundo documento")
        
        #teste quando possui maiusculas e minusculas (deve-se contabilizar não importando maiusculas e minusculas)
        wcount.checkWord(document, "de")
        wcount.checkWord(document, "DE")
        wcount.checkWord(document, "Do")
        wcount.checkWord(document, "ui")
        int_result = wcount.compute_feature(document)
        self.assertEqual(int_result, 3, "Nao foi contabilizado o numero de palavras corretos no teste do terceiro documento")

        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'TestFeatureCalculator.testName']
    unittest.main()