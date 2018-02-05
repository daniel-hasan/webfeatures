'''
Created on 13 de nov de 2017
Testes da contagem de tags em HTML
@author: Beatriz Souza da Silva beatrizsouza_dasilva@hotmail.com
'''
import unittest
from feature.language_dependent_words.featureImpl.structure_features import TagCountFeature
from feature.features import ParserTags
from feature.features import FeatureVisibilityEnum, Document, TagBasedFeature
from utils.basic_entities import FormatEnum, FeatureTimePerDocumentEnum

class TestTagCounter(unittest.TestCase):
    

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
    
    def testTag(self):
        tcount = TagCountFeature("contagem de tags", "Feature que conta tags em HTML", "HTML", 
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.HTML, 
                                         FeatureTimePerDocumentEnum.MILLISECONDS,["head","body"])
    
        tcount2 = TagCountFeature("contagem de tags doc 2", "Feature que conta tags em HTML", "HTML", 
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.HTML, 
                                         FeatureTimePerDocumentEnum.MILLISECONDS,["p"])
        
        document = Document(1,"doc1","O texto nao precisa -necessariamente - ser o texto que sera testado")
        
        tcount.checkTag(document, "head")
        '''feed vai pegar somente o nome da tag, sem <>'''
        tcount.checkTag(document,"Teste")
        tcount.checkTag(document,"body")
        tcount.checkTag(document,"p")
        int_result = tcount.compute_feature(document)
        self.assertEqual(int_result, 2, "Nao foi contabilizado o numero de palavras corretos no teste do terceiro documento")
        
        tcount2.checkTag(document, "head")
        tcount2.checkTag(document,"Teste")
        tcount2.checkTag(document,"body")
        tcount2.checkTag(document,"p")
        int_result = tcount2.compute_feature(document)
        self.assertEqual(int_result, 1, "Nao foi contabilizado o numero de palavras corretos no teste do terceiro documento")

class TestParserTags(unittest.TestCase):
    def testParser(self):
        tcount = TagCountFeature("contagem de tags", "Feature que conta tags em HTML", "HTML", 
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.HTML, 
                                         FeatureTimePerDocumentEnum.MILLISECONDS,["head","body"])
        document = Document(1,"doc1","O texto nao precisa -necessariamente - ser o texto que sera testado")
        parser = ParserTags(tcount,document)
        parser.feed("<head></head><body>Dados de teste</body><p>Parágrafo</p>")

    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'TestFeatureCalculator.testName']
    unittest.main()
    
