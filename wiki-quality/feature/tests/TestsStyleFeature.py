'''
Created on 4 de set de 2017
Testes de todas as classes abstratas de calculo das features
@author: Daniel Hasan Dalip hasan@decom.cefetmg.br
'''
from os import linesep
import unittest

from feature.featureImpl.style_features import WordCountFeature, \
    SentenceCountFeature, LargeSentenceCountFeature, ParagraphCountFeature, \
    LargeParagraphCountFeature, CharacterCountFeature, SyllableCountFeature,\
    WordsSyllablesCountFeature
from feature.features import FeatureVisibilityEnum, Document, \
    SentenceBasedFeature
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
    
    
    def testParagraph(self):
        
        document = Document(1,"doc1","texto do paragrafo")
        
        parcount = ParagraphCountFeature("teste de paragrafos","testinho de paragrafos",
                                         "paragrafo",
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS)
        parcountlarge = LargeParagraphCountFeature("teste de paragrafos grandes","testinho de grandes paragrafos",
                                         "paragrafo grande",
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS,16)
        parcount.checkParagraph(document, "Paragrafo com uma linha.\n")
        parcount.checkParagraph(document, "Paragrafo com a primeira frase. Paragrafo com a segunda frase. \n")
        parcount.checkParagraph(document, "Paragrafo com a primeira frase. Paragrafo com a segunda frase. Sem espaço no final.\n")
        
        int_result_larger = parcount.compute_feature(document)
        self.assertEqual(int_result_larger, 3, "Nao foi contabilizado o numero de paragrafos corretos no teste do primeiro documento")
 
        
        parcountlarge.checkWord(document, "Paragrafo")
        parcountlarge.checkWord(document, " ")
        parcountlarge.checkWord(document, "pequeno")
        parcountlarge.checkWord(document, ".")
        parcountlarge.checkWord(document, linesep)
        
        int_result_larger = parcountlarge.compute_feature(document)
        parcount.finish_document(document)
        self.assertEqual(int_result_larger, 0, "Nao foi contabilizado o numero de paragrafos grandes corretas no teste do segundo documento")
 
        
        parcountlarge.checkWord(document, "Um")
        parcountlarge.checkWord(document, " ")
        parcountlarge.checkWord(document, "Dois")
        parcountlarge.checkWord(document, " ")
        parcountlarge.checkWord(document, "três")
        parcountlarge.checkWord(document, " ")
        parcountlarge.checkWord(document, "quatro")
        parcountlarge.checkWord(document, " ")
        parcountlarge.checkWord(document, "cinco")
        parcountlarge.checkWord(document, " ")
        parcountlarge.checkWord(document, "seis")
        parcountlarge.checkWord(document, " ")
        parcountlarge.checkWord(document, "sete")
        parcountlarge.checkWord(document, " ")
        parcountlarge.checkWord(document, "oito")
        parcountlarge.checkWord(document, " ")
        parcountlarge.checkWord(document, "nove")
        parcountlarge.checkWord(document, " ")
        parcountlarge.checkWord(document, "dez")
        parcountlarge.checkWord(document, " ")
        parcountlarge.checkWord(document, "onze")
        parcountlarge.checkWord(document, " ")
        parcountlarge.checkWord(document, "doze")
        parcountlarge.checkWord(document, " ")
        parcountlarge.checkWord(document, "treze")
        parcountlarge.checkWord(document, " ")
        parcountlarge.checkWord(document, "catorze")
        parcountlarge.checkWord(document, " ")
        parcountlarge.checkWord(document, "quinze")
        parcountlarge.checkWord(document, " ")
        parcountlarge.checkWord(document, "dezesseis")
        parcountlarge.checkWord(document, " ")
        parcountlarge.checkWord(document, "dezessete")
        parcountlarge.checkWord(document, linesep)
        
        int_result_larger = parcountlarge.compute_feature(document)
        parcountlarge.finish_document(document)
        self.assertEqual(int_result_larger, 1, "Nao foi contabilizado o numero de paragrafos grandes corretos no teste do segundo documento")
 
               
        parcountlarge.checkWord(document, "Paragrafo")
        parcountlarge.checkWord(document, " ")
        parcountlarge.checkWord(document, "pequeno")
        parcountlarge.checkWord(document, ".")
        parcountlarge.checkWord(document, "\n")
        parcountlarge.checkWord(document, "Um")
        parcountlarge.checkWord(document, " ")
        parcountlarge.checkWord(document, "Dois")
        parcountlarge.checkWord(document, " ")
        parcountlarge.checkWord(document, "três")
        parcountlarge.checkWord(document, " ")
        parcountlarge.checkWord(document, "quatro")
        parcountlarge.checkWord(document, " ")
        parcountlarge.checkWord(document, "cinco")
        parcountlarge.checkWord(document, " ")
        parcountlarge.checkWord(document, "seis")
        parcountlarge.checkWord(document, " ")
        parcountlarge.checkWord(document, "sete")
        parcountlarge.checkWord(document, " ")
        parcountlarge.checkWord(document, "oito")
        parcountlarge.checkWord(document, " ")
        parcountlarge.checkWord(document, "nove")
        parcountlarge.checkWord(document, " ")
        parcountlarge.checkWord(document, "dez")
        parcountlarge.checkWord(document, " ")
        parcountlarge.checkWord(document, "onze")
        parcountlarge.checkWord(document, " ")
        parcountlarge.checkWord(document, "doze")
        parcountlarge.checkWord(document, " ")
        parcountlarge.checkWord(document, "treze")
        parcountlarge.checkWord(document, " ")
        parcountlarge.checkWord(document, "catorze")
        parcountlarge.checkWord(document, " ")
        parcountlarge.checkWord(document, "quinze")
        parcountlarge.checkWord(document, " ")
        parcountlarge.checkWord(document, "dezesseis")
        parcountlarge.checkWord(document, " ")
        parcountlarge.checkWord(document, "dezessete")
        parcountlarge.checkWord(document, linesep)
        
        int_result_larger = parcountlarge.compute_feature(document)
        parcountlarge.finish_document(document)
        self.assertEqual(int_result_larger, 1, "Nao foi contabilizado o numero de paragrafos grandes corretos no teste do segundo documento")
 
        
    def testSentenceCountTest(self):
        sentcount = SentenceCountFeature("teste de frases","testinho de frases","testão graças a Deus",
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS)
        
        sentcountlarge = LargeSentenceCountFeature("teste de frases grandes","testinho de frases grandes",
                                                   "testão de frases grandes graças a Deus",
                                                   FeatureVisibilityEnum.public, FormatEnum.text_plain, 
                                                   FeatureTimePerDocumentEnum.MILLISECONDS, 9)
        document = Document(1,"doc1","lembrando que não é o teste de fato")
        
        sentcount.checkSentence(document, "Frase pequena!")
        sentcount.checkSentence(document, "Frase de tamanho razoavelmente normal, com conteúdo satisfatório.")
        sentcount.checkSentence(document, "Frase com conteúdo enorme, com várias virgulas, várias coisas sem sentido, gigantesca, enorme e muito feia.")
        sentcount.checkSentence(document, " Será que com espaço isso continua funcionando hein ? ")
        
        int_result = sentcount.compute_feature(document)
        sentcount.finish_document(document)
        self.assertEqual(int_result, 4, "Nao foi contabilizado o numero de frases corretas no teste do primeiro documento")
        
        sentcountlarge.checkWord(document, "Frase")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "pequena")
        sentcountlarge.checkWord(document, "!")
        
        int_result_larger = sentcountlarge.compute_feature(document)
        sentcountlarge.finish_document(document)
        self.assertEqual(int_result_larger, 0, "Nao foi contabilizado o numero de frases grandes corretas no teste do segundo documento")
 
        
        sentcountlarge.checkWord(document, "Frase")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "com")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "conteúdo")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "enorme")
        sentcountlarge.checkWord(document, ",")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "com")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "várias")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "virgulas")
        sentcountlarge.checkWord(document, ",")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "várias")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "coisas")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "sem")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "sentido")
        sentcountlarge.checkWord(document, ",")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "gigantesca")
        sentcountlarge.checkWord(document, ",")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "enorme")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "e")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "muito")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "feia")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, ".")
        
        int_result_larger = sentcountlarge.compute_feature(document)
        sentcountlarge.finish_document(document)
        self.assertEqual(int_result_larger, 1,
                          "Nao foi contabilizado o numero de frases grandes corretas no teste do segundo documento")
        
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "Será")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "que")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "com")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "espaço")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "isso")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "continua")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "funcionando")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "hein")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "?")
        sentcountlarge.checkWord(document, " ")
        
        int_result_larger = sentcountlarge.compute_feature(document)
        sentcountlarge.finish_document(document)
        self.assertEqual(int_result_larger, 0, "Nao foi contabilizado o numero de frases grandes corretas no teste do segundo documento")
        
        
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "Será")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "que")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "com")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "espaço")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "isso")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "continua")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "funcionando")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "hein")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, " ")
        self.assertEqual(sentcountlarge.int_word_counter, 8, "Deveria contar apenas ass palavras e nao os espacos =P")
        sentcountlarge.checkWord(document, "?")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "Frase")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "com")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "conteúdo")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "enorme")
        sentcountlarge.checkWord(document, ",")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "com")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "várias")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "virgulas")
        sentcountlarge.checkWord(document, ",")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "várias")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "coisas")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "sem")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "sentido")
        sentcountlarge.checkWord(document, ",")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "gigantesca")
        sentcountlarge.checkWord(document, ",")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "enorme")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "e")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "muito")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "feia")
        sentcountlarge.checkWord(document, ".")
        sentcountlarge.checkWord(document, "Frase")
        sentcountlarge.checkWord(document, " ")
        sentcountlarge.checkWord(document, "pequena")
        sentcountlarge.checkWord(document, "!")
        
        
        int_result_larger = sentcountlarge.compute_feature(document)
        sentcountlarge.compute_feature(document)
        self.assertEqual(int_result_larger, 1, "Nao foi contabilizado o numero de frases grandes corretas no teste do segundo documento")
        
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
        wcount.finish_document(document)
        self.assertEqual(int_result, 3, "Nao foi contabilizado o numero de palavras corretos no teste do primeiro documento")
        
        #teste quando o texto não possul palavra alguma
        int_result = wcount.compute_feature(document)
        wcount.finish_document(document)
        self.assertEqual(int_result, 0, "Nao foi contabilizado o numero de palavras corretos no teste do segundo documento")
        
        #teste quando possui maiusculas e minusculas (deve-se contabilizar não importando maiusculas e minusculas)
        wcount.checkWord(document, "de")
        wcount.checkWord(document, "DE")
        wcount.checkWord(document, "Do")
        wcount.checkWord(document, "do")
        wcount.checkWord(document, "ui")
        int_result = wcount.compute_feature(document)
        wcount.finish_document(document)
        self.assertEqual(int_result, 2, "Nao foi contabilizado o numero de palavras corretos no teste do terceiro documento")
    
    def testCharCount(self):
        ccount = CharacterCountFeature("ola feature contadora", "Essa feature é divertitida", 
                                         "SILVA Ola. Contando Olas. Conferencia dos Hello World", 
                                         FeatureVisibilityEnum.public, FormatEnum.text_plain, 
                                         FeatureTimePerDocumentEnum.MILLISECONDS)
        
        document = Document(1,"doc1","O texto nao precisa -necessariamente - ser o texto que sera testado")
        
        ccount.checkChar(document, "T")
        ccount.checkChar(document, "e")
        ccount.checkChar(document, "m")
        ccount.checkChar(document, "q")
        ccount.checkChar(document, " ")
        ccount.checkChar(document, "d")
        ccount.checkChar(document, "a")
        ccount.checkChar(document, "r")
        ccount.checkChar(document, " ")
        ccount.checkChar(document, "1")
        ccount.checkChar(document, "2")
        ccount.checkChar(document, ".")
        int_result = ccount.compute_feature(document)
        ccount.finish_document(document)
        self.assertEqual(int_result, 12, "Nao foi contabilizado o numero de chars corretos no teste do primeiro documento")
        
        ccount.checkChar(document, "T")
        ccount.checkChar(document, "e")
        ccount.checkChar(document, "m")
        ccount.checkChar(document, "q")
        ccount.checkChar(document, " ")
        ccount.checkChar(document, "d")
        ccount.checkChar(document, "a")
        ccount.checkChar(document, "r")
        ccount.checkChar(document, " ")
        ccount.checkChar(document, "1")
        ccount.checkChar(document, "1")
        int_result = ccount.compute_feature(document)
        ccount.finish_document(document)
        self.assertEqual(int_result, 11, "Nao foi contabilizado o numero de chars corretos no teste do segundo documento")
        
    
    def testSyllableCount(self):
        scount = SyllableCountFeature("ola feature contadora", "Essa feature é divertitida", 
                                         "SILVA Ola. Contando Olas. Conferencia dos Hello World", 
                                         FeatureVisibilityEnum.public, FormatEnum.text_plain, 
                                         FeatureTimePerDocumentEnum.MILLISECONDS)
        
        complexcount = WordsSyllablesCountFeature("ola feature contadora", "Essa feature é divertitida", 
                                         "SILVA Ola. Contando Olas. Conferencia dos Hello World", 
                                         FeatureVisibilityEnum.public, FormatEnum.text_plain, 
                                         FeatureTimePerDocumentEnum.MILLISECONDS, 3)
        
        policount = WordsSyllablesCountFeature("ola feature contadora", "Essa feature é divertitida", 
                                         "SILVA Ola. Contando Olas. Conferencia dos Hello World", 
                                         FeatureVisibilityEnum.public, FormatEnum.text_plain, 
                                         FeatureTimePerDocumentEnum.MILLISECONDS, 4)
        
        document = Document(1,"doc1","O texto nao precisa -necessariamente - ser o texto que sera testado")
        
        scount.checkWord(document, "I")
        scount.checkWord(document, "don't")
        scount.checkWord(document, "know")
        scount.checkWord(document, "how")
        int_result = scount.compute_feature(document)
        scount.finish_document(document)
        self.assertEqual(int_result, 4, "O numero de silabas do primeiro documento não está correto")
        
        scount.checkWord(document, "purple")
        scount.checkWord(document, "perfect")
        scount.checkWord(document, "sixty")
        scount.checkWord(document, "Godard")
        scount.checkWord(document, "tuesday")
        scount.checkWord(document, "189")
        int_result = scount.compute_feature(document)
        scount.finish_document(document)
        self.assertEqual(int_result, 11, "O numero de silabas do segundo documento não está correto")
        
        complexcount.checkWord(document, "Family")
        complexcount.checkWord(document, "Animal")
        complexcount.checkWord(document, "identical")
        complexcount.checkWord(document, "now")
        int_result = complexcount.compute_feature(document)
        complexcount.finish_document(document)
        self.assertEqual(int_result, 3, "O numero de palavras complexas do primeiro documento não está correto")
        
        complexcount.checkWord(document, "secretary")
        complexcount.checkWord(document, "Undemanding")
        complexcount.checkWord(document, "cat")
        complexcount.checkWord(document, "dog")
        complexcount.checkWord(document, "hey")
        int_result = complexcount.compute_feature(document)
        complexcount.finish_document
        self.assertEqual(int_result, 2, "O numero de palavras complexas do segundo documento não está correto")
        
        policount.checkWord(document, "irregular")
        policount.checkWord(document, "Watermelon")
        policount.checkWord(document, "roll")
        policount.checkWord(document, "fat")
        int_result = policount.compute_feature(document)
        policount.finish_document(document)
        self.assertEqual(int_result, 2, "O numero de polissilabas do primeiro documento não está correto")
        
        policount.checkWord(document, "macaronic")
        policount.checkWord(document, "Intermittent")
        policount.checkWord(document, "environment")
        policount.checkWord(document, "alligator")
        policount.checkWord(document, "alternative")
        int_result = policount.compute_feature(document)
        policount.finish_document(document)
        self.assertEqual(int_result, 5, "O numero de polissilabas do segundo documento não está correto")
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'TestFeatureCalculator.testName']
    unittest.main()