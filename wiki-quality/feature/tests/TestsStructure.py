'''
Created on 13 de nov de 2017
Testes da contagem de tags em HTML
@author: Beatriz Souza da Silva beatrizsouza_dasilva@hotmail.com
'''
from statistics import mean, stdev
import unittest

from feature.featureImpl.structure_features import TagCountFeature, \
    SectionSizeFeature, AverageSectionSize, StdDeviationSectionSize, \
    LargestSectionSize, ShortestSectionSize
from feature.features import FeatureVisibilityEnum, Document, TagBasedFeature
from feature.features import ParserTags
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
    
    def testTagCounter(self):
        '''
        Created on 13 de nov de 2017
        Testes da contagem de tags em HTML
        @author: Beatriz Souza da Silva beatrizsouza_dasilva@hotmail.com
        '''
        tcount = TagCountFeature("contagem de tags", "Feature que conta tags em HTML", "HTML", 
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.HTML, 
                                         FeatureTimePerDocumentEnum.MILLISECONDS,["head","body"])
    
        tcount2 = TagCountFeature("contagem de tags doc 2", "Feature que conta tags em HTML", "HTML", 
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.HTML, 
                                         FeatureTimePerDocumentEnum.MILLISECONDS,["p"])
        
        document = Document(1,"doc1","O texto nao precisa -necessariamente - ser o texto que sera testado")
        
        tcount.startTag(document, "head",[])
        '''feed vai pegar somente o nome da tag, sem <>'''
        tcount.startTag(document,"Teste",[])
        tcount.startTag(document,"body",[])
        tcount.startTag(document,"p",[])
        int_result = tcount.compute_feature(document)
        self.assertEqual(int_result, 2, "Nao foi contabilizado o numero de palavras corretos no teste do terceiro documento")
        
        tcount2.startTag(document, "head",[])
        tcount2.startTag(document,"Teste",[])
        tcount2.startTag(document,"body",[])
        tcount2.startTag(document,"p",[])
        int_result = tcount2.compute_feature(document)
        self.assertEqual(int_result, 1, "Nao foi contabilizado o numero de palavras corretos no teste do terceiro documento")
class SectionSizeTest(SectionSizeFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,intSectionLevel):
        super().__init__(name,description,reference,visibility,text_format,feature_time_per_document,intSectionLevel)
        self.arrSectionSizes = []
        
    def lastSectionSize(self,intSectionSize):
        self.arrSectionSizes.append(intSectionSize)
    
    def compute_feature(self, document):
        super().compute_feature(document)
        aux = self.arrSectionSizes
        self.arrSectionSizes = []
        return aux
    
        
class TestSectionFeatures(unittest.TestCase):
    DOCUMENTS = [Document(1,"doc1","<h1> oioioi<h2123>lalalal</h1>O texto da seç&atilde;o<h2222></h2222> ete aqui<h1>oioi</h1>nova seção"),
                 Document(2,"doc1","<h2>subseção sem seção</h2> esta é uma subseção"+
                                    "<h1>seção</h1>esta nova seção"+
                                        "<h2>xxx</h2>"+
                                            "novo novo<h1>maio umas</h1>xuxu"),
                 ]     
    SECTION_SIZES =  [[25,10],[27,4]]
    SUB_SECTION_SIZES =  [[],[20,9]]
      
    def assert_section_sizes(self,objFeature,arrResultPerDoc,strResult):
        arrFeaturesResult = []
        

        
        for document in TestSectionFeatures.DOCUMENTS:
            parser = ParserTags(objFeature,document)
            parser.feed(document.str_text)
            arrSizes = parser.feat.compute_feature(document)
            arrFeaturesResult.append(arrSizes)
            parser.feat.finish_document(document)
            
        #teste seção
        for intI in range(len(arrResultPerDoc)):
            if(type(arrResultPerDoc[intI]) == list):
                self.assertListEqual(arrFeaturesResult[intI], arrResultPerDoc[intI], strResult.format(document_num=0,result=str(arrFeaturesResult[0]),expected=str(arrResultPerDoc[intI])))
            else:
                self.assertEqual(arrFeaturesResult[intI], arrResultPerDoc[intI], strResult.format(document_num=0,result=str(arrFeaturesResult[0]),expected=str(arrResultPerDoc[intI])))

        
        #teste subseção
        
    def testSectionSizeFeature(self):
        '''
        Created on 20 de fev de 2018
        Verifica se o tamanho da seção está sendo calculado corretamente
        @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
        '''
        
        sizeLevel1 = SectionSizeTest("Section ", "Section size in array", "HTML", 
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.HTML, 
                                         FeatureTimePerDocumentEnum.MILLISECONDS,1)
        
        self.assert_section_sizes(sizeLevel1, TestSectionFeatures.SECTION_SIZES, "O tamanho das seções (h1 tags) do documento {document_num} estao errados! Deveriam ser:{expected} e foi:{result}")
        
        
        sizeLevel2 = SectionSizeTest("SubSection size", "SubSection size in array", "HTML", 
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.HTML, 
                                         FeatureTimePerDocumentEnum.MILLISECONDS,2)
        
        self.assert_section_sizes(sizeLevel2, TestSectionFeatures.SUB_SECTION_SIZES, "O tamanho das subseções (h2 tags) do documento {document_num} estao errados! Deveriam ser:{expected} e foi:{result}")

    def assert_section_feature(self,FeatureClass,arrResultsSection,arrResultsSubsection,strMetricName):
        avgSectionSize1 = FeatureClass(strMetricName+" Section Size", "The ratio between the section sizes (in chars) and the section count", "HTML", 
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.HTML, 
                                         FeatureTimePerDocumentEnum.MILLISECONDS,1)
        
        self.assert_section_sizes(avgSectionSize1, arrResultsSection, "Erro no calculo do(a) "+strMetricName+" das seções (h1 tags) do documento {document_num} estao errados! Deveria ser:{expected} e foi:{result}")

        
        avgSectionSize2 = FeatureClass(strMetricName+" Sub-section Size", "The ratio between the subsection sizes (in chars) and the section count", "HTML",
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.HTML, 
                                         FeatureTimePerDocumentEnum.MILLISECONDS,2)
      
        self.assert_section_sizes(avgSectionSize2, arrResultsSubsection, "Erro no calculo do(a) "+strMetricName+" das subseções (h2 tags) do documento {document_num} estao errados! Deveria ser:{expected} e foi:{result}")
        

    def testAverageAndStdSectionSizeFeature(self):
        '''
        Created on 20 de fev de 2018
        Verifica se a media e o desvio padrao da seção/subseção está sendo calculada corretamente
        @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
        '''
        #calcula e testa a media
        arrResultsSection= [mean(arrSizes) if len(arrSizes)!=0 else 0 for arrSizes in TestSectionFeatures.SECTION_SIZES]
        arrResultsSubSection= [mean(arrSizes) if len(arrSizes)!=0 else 0 for arrSizes in TestSectionFeatures.SUB_SECTION_SIZES]
        self.assert_section_feature(AverageSectionSize, arrResultsSection, arrResultsSubSection, "média")
                
        #calcula e testa o desvio padrao
        arrResultsSection= [stdev(arrSizes) if len(arrSizes)!=0 else 0 for arrSizes in TestSectionFeatures.SECTION_SIZES]
        arrResultsSubSection= [stdev(arrSizes) if len(arrSizes)!=0 else 0 for arrSizes in TestSectionFeatures.SUB_SECTION_SIZES]
        self.assert_section_feature(StdDeviationSectionSize, arrResultsSection, arrResultsSubSection, "desvio padrão")
                
    def testMaxMinSizeFeature(self):
        '''
        Created on 20 de fev de 2018
        Verifica se o tamanho da seção minima e maxima está sendo calculada corretamente
        @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
        '''
        #calcula e testa o minimo
        arrResultsSection= [min(arrSizes) if len(arrSizes)!=0 else 0 for arrSizes in TestSectionFeatures.SECTION_SIZES]
        arrResultsSubSection= [min(arrSizes) if len(arrSizes)!=0 else 0 for arrSizes in TestSectionFeatures.SUB_SECTION_SIZES]
        self.assert_section_feature(ShortestSectionSize, arrResultsSection, arrResultsSubSection, "mínimo")
                
        #calcula e testa o desvio padrao
        arrResultsSection= [max(arrSizes) if len(arrSizes)!=0 else 0 for arrSizes in TestSectionFeatures.SECTION_SIZES]
        arrResultsSubSection= [max(arrSizes) if len(arrSizes)!=0 else 0 for arrSizes in TestSectionFeatures.SUB_SECTION_SIZES]
        self.assert_section_feature(LargestSectionSize, arrResultsSection, arrResultsSubSection, "máximo")
        #arrResultsSection= [mean(arrSizes) if len(arrSizes)!=0 else 0 for arrSizes in TestSectionFeatures.SECTION_SIZES]
        #arrResultsSubSection= [mean(arrSizes) if len(arrSizes)!=0 else 0 for arrSizes in TestSectionFeatures.SECTION_SIZES]
        #self.assert_section_feature(AverageSectionSize, arrResultsSection, arrResultsSubSection, "média")
        
        
                
class TestParserTags(unittest.TestCase):
    def testParser(self):
        tcount = TagCountFeature("contagem de tags", "Feature que conta tags em HTML", "HTML", 
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.HTML, 
                                         FeatureTimePerDocumentEnum.MILLISECONDS,["p","h1"])
        document = Document(1,"doc1","O texto nao precisa -necessariamente - ser o texto que sera testado")
        parser = ParserTags(tcount,document)
        parser.feed("<head></head><body>Dados<p>Parágrafo</p><h1><h123> de teste</body>")
        intValFeature = parser.feat.compute_feature(document)
        self.assertEqual(intValFeature, 2, "Nao foi contabilizado o numero de seções (h1) e paragrafos (p)"+
                         " no documento testado. Seriam 2 tags e o resultado foi: "+str(intValFeature))

        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'TestFeatureCalculator.testName']
    unittest.main()
    
