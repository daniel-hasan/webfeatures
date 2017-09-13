'''
Created on 4 de set de 2017
Testes de todas as classes abstratas de calculo das features
@author: Daniel Hasan Dalip hasan@decom.cefetmg.br
'''

import unittest

from feature.features import FeatureDocumentsReader, FeatureVisibilityEnum, \
    WordBasedFeature, TextBasedFeature, FeatureDocumentsWriter, Document, \
    FeatureCalculator
from utils.basic_entities import FormatEnum, FeatureTimePerDocumentEnum


class DocSetReaderForTest(FeatureDocumentsReader):
    '''
    Created on 4 de set de 2017
    Criei um reader novo. Assim, ao testar o TestFeatureCalculator garantimos que o teste não seja afetado caso o reader (oficial) esteja errado.
    Depois, temos que fazer um teste para ver se o(s) reader(s) (oficial) está funcionando
    @author: Daniel Hasan Dalip hasan@decom.cefetmg.br
    '''
    def get_documents(self):
        yield Document(1,"doc1","Ola, meu nome é hasan")
        yield Document(2,"doc2","ipi ipi ura")
        yield Document(3,"doc3","lalala")

class DocWriterForTest(FeatureDocumentsWriter):
    '''
    Created on 4 de set de 2017
    Criei um writer novo pelo mesmo motivo de ter criado um reader novo.
    Este writer vai apenas gravar (em memória) para podemos fazer os testes.
    O result é um atributo que é um mapa em que a chave é o nome do documento
    e o valor são todos  os resultados do mesmo
    @author: Daniel Hasan Dalip hasan@decom.cefetmg.br
    '''
    def __init__(self):
        self.result = {}
        
    def write_document(self,document, arr_feats_used, arr_feats_result):
        self.result[document.str_doc_name] = arr_feats_result

class WordTestFeature(WordBasedFeature):
    '''
    Classe para usar no teste que verifica se o WordBasedFeature está funcionando. 
    '''
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super(WordBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)
        self.arr_str_words = []  
        
          
    def checkWord(self,document,word):
        self.arr_str_words.append(word)
    
    def feature_result(self,document):
        arr_aux = self.arr_str_words
        self.arr_str_words = []      
        return arr_aux
class TextTestFeature(TextBasedFeature):
    '''
    Classe para usar no teste que verifica se o WordBasedFeature está funcionando. 
    '''
    def compute_feature(self,document):
        return document.str_text

    
'''
Essa classe seria para testar o SentenceBasedFeature está funcionadno - implementar
o SentenceBasedFeature em features.py primeiro
class SentenceTestFeature(SentenceBasedFeature):
    
    Classe para usar no teste que verifica se o WordBasedFeature está funcionando. 
    
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super(SentenceBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)
        self.arr_str_sentence = []  
        
          
    def checkSentence(self,document,sentence):
        self.arr_str_sentence.append(sentence)
    
    def feature_result(self,document):
        arr_aux = self.arr_str_sentence
        self.arr_str_sentence = []      
        return arr_str_sentence    
'''    

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


    def testLeitura(self):
        '''
            Sugestão: use uma feature word based, outra textbased e outra sentence based
            assim, testamos todas as alternativas. Coloque mensagens de erro explicando exatamente
            onde o erro ocorreu. Note que neste método você não precisa se preocupar 
            se uma feature está sendo calculada e sim se o featureCalculator está funcionando: 
            ou seja, se for text based, se está extraindo todo o texto
                    se for sentence based, se está extraindo cada frase
                    se for word based, se está extraindo toda as palavras
            por isso, criamos três classes (WordExtractFeature, SentenceExtractFeature e TextExtractFeature 
            para testar - será também independente).
        '''
        arr_features = [WordTestFeature("ola feature", "Essa feature é divertitida", 
                                         "SILVA Ola. Contando Olas. Conferencia dos Hello World", 
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.text_plain, 
                                         FeatureTimePerDocumentEnum.MILLISECONDS),
                        TextTestFeature("outra feature legal", "Essa feature é divertitida", 
                                         "SILVA Ola. Contando Olas. Conferencia dos Hello World", 
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.text_plain, 
                                         FeatureTimePerDocumentEnum.MILLISECONDS),
                        #SentenceTestFeature("outra feature legal sentence", "Essa feature é divertitida", 
                        #                 "SILVA Ola. Contando Olas. Conferencia dos Hello World", 
                        #                 FeatureVisibilityEnum.public, 
                        #                 FormatEnum.text_plain, 
                        #                 FeatureTimePerDocumentEnum.MILLISECONDS)
                        ]
        obj_writer = DocWriterForTest()
        FeatureCalculator.featureManager.computeFeatureSetDocuments(DocSetReaderForTest(),
                                                                    obj_writer,
                                                                    arr_features,
                                                                    FormatEnum.text_plain
                                                                    )
        map_result = obj_writer.result
        
        self.assertListEqual(map_result["doc1"][0], ["Ola",","," ","meu"," ","nome"," ","é"," ","hasan"]
                                                     , "A leitura das palavras está incorreta"
                                                     )
        self.assertListEqual(map_result["doc1"][0], "Ola meu nome é hasan", "A leitura do texto está incorreto")
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'TestFeatureCalculator.testName']
    unittest.main()