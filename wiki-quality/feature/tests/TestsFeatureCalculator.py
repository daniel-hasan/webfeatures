'''
Created on 4 de set de 2017
Testes de todas as classes abstratas de calculo das features
@author: Daniel Hasan Dalip hasan@decom.cefetmg.br
'''

import unittest

from feature.features import *
from utils.basic_entities import FormatEnum, FeatureTimePerDocumentEnum
from cmd_line_interface.CaracterInterface import *


class DocSetReaderForTest(FeatureDocumentsReader):
    '''
    Created on 4 de set de 2017
    Criei um reader novo. Assim, ao testar o TestFeatureCalculator garantimos que o teste não seja afetado caso o reader (oficial) esteja errado.
    Depois, temos que fazer um teste para ver se o(s) reader(s) (oficial) está funcionando
    @author: Daniel Hasan Dalip hasan@decom.cefetmg.br
    '''
    def get_documents(self):
        yield Document(1,"doc1","Ola, meu nome é hasan.")
        yield Document(2,"doc2","ipi ipi ura. Duas frases no texto.")
        yield Document(3,"doc3","lalala.\nMeu teste tem tres paragrafos.\nEsse é o último.\n")
        yield Document(4,"doc4","lalala.\nMeu teste tem tres paragrafos.\nEsse é o último")
        yield Document(5,"doc5","<p>Ola        ,      meu nome é hasan.</p>")
        yield Document(6,"doc6","<head></head><body><p>Meu</p><p>teste de palavras.</p></body>")

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

class CharTestFeature(CharBasedFeature):
    '''
    Classe para usar no teste que verifica se o CharBasedFeature está funcionando.
    '''
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super(CharBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)
        self.arr_str_char = []

    def checkChar(self,document,char):
        self.arr_str_char.append(char)
        return True

    def compute_feature(self,document):
        arr_aux = self.arr_str_char

        return arr_aux

    def finish_document(self, document):
        self.arr_str_char = []

class WordTestFeature(WordBasedFeature):
    '''
    Classe para usar no teste que verifica se o WordBasedFeature está funcionando.
    '''
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super(WordBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)
        self.arr_str_words = []


    def checkWord(self,document,word):
        self.arr_str_words.append(word)
        return True

    def compute_feature(self,document):
        arr_aux = self.arr_str_words
        return arr_aux

    def finish_document(self, document):
        self.arr_str_words = []
class SentenceTestFeature(SentenceBasedFeature):
    '''
    Classe para usar no teste que verifica se o SentenceBasedFeature está funcionando.
    '''

    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super(SentenceBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)
        self.arr_str_sentence = []


    def checkSentence(self,document,sentence):
        #print("SENTENCA:  "+sentence)
        self.arr_str_sentence.append(sentence)
        return True

    def compute_feature(self,document):
        arr_aux = self.arr_str_sentence

        return arr_aux

    def finish_document(self, document):
        self.arr_str_sentence = []

class ParagraphTestFeature(ParagraphBasedFeature):

    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super(ParagraphBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)
        self.arr_str_paragraph = []


    def checkParagraph(self,document,paragraph):
        self.arr_str_paragraph.append(paragraph)
        return True

    def compute_feature(self,document):
        arr_aux = self.arr_str_paragraph

        return arr_aux

    def finish_document(self, document):
        self.arr_str_paragraph = []

class TagTestFeature(TagBasedFeature):

    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super(TagBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)
        self.arr_str_tag = []


    def startTag(self,document, tag, attrs):
        self.arr_str_tag.append(tag)
        return True

    def compute_feature(self,document):
        arr_aux = self.arr_str_tag
        return arr_aux
    def finish_document(self, document):
        self.arr_str_tag = []
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
                        SentenceTestFeature("outra feature legal", "Essa feature é divertitida",
                                         "SILVA Ola. Contando Olas. Conferencia dos Hello World",
                                         FeatureVisibilityEnum.public,
                                         FormatEnum.text_plain,
                                         FeatureTimePerDocumentEnum.MILLISECONDS),

                        ParagraphTestFeature("outra feature legal", "Essa feature é divertitida",
                                         "SILVA Ola. Contando Olas. Conferencia dos Hello World",
                                         FeatureVisibilityEnum.public,
                                         FormatEnum.text_plain,
                                         FeatureTimePerDocumentEnum.MILLISECONDS),

                        WordTestFeature("tag feature", "Essa feature é divertitida",
                                         "SILVA Ola. Contando Olas. Conferencia dos Hello World",
                                         FeatureVisibilityEnum.public,
                                         FormatEnum.HTML,
                                         FeatureTimePerDocumentEnum.MILLISECONDS),

                        TagTestFeature("tag legal feature", "Essa feature é divertitida",
                                         "SILVA Ola. Contando Olas. Conferencia dos Hello World",
                                         FeatureVisibilityEnum.public,
                                         FormatEnum.HTML,
                                         FeatureTimePerDocumentEnum.MILLISECONDS),
                        CharTestFeature("char legal feature", "Essa feature é divertitida",
                                         "SILVA Ola. Contando Olas. Conferencia dos Hello World",
                                         FeatureVisibilityEnum.public,
                                         FormatEnum.HTML,
                                         FeatureTimePerDocumentEnum.MILLISECONDS)
                        ]
        obj_writer = DocWriterForTest()
        FeatureCalculator.featureManager.computeFeatureSetDocuments(DocSetReaderForTest(),
                                                                    obj_writer,
                                                                    arr_features,
                                                                    FormatEnum.HTML
                                                                    )
        map_result = obj_writer.result

        self.assertListEqual(map_result["doc1"][0], ["Ola",",","meu","nome","é","hasan","."]
                                                     , "A leitura das palavras está incorreta"
                                                     )
        self.assertListEqual(map_result["doc1"][1], ["Ola, meu nome é hasan."], "A leitura do texto está incorreto")
        self.assertListEqual(map_result["doc4"][1], ["lalala.","\nMeu teste tem tres paragrafos.","\nEsse é o último"], "A leitura do texto está incorreto")
        self.assertListEqual(map_result["doc4"][2], ["lalala.","Meu teste tem tres paragrafos.","Esse é o último"], "A leitura do texto está incorreto")
        self.assertListEqual(map_result["doc1"][2], ["Ola, meu nome é hasan."], "A leitura do texto está incorreto")

        '''Testam se o HTML está sendo limpo'''
        self.assertListEqual(map_result["doc5"][3], ["Ola",",","meu","nome","é","hasan","."],"A leitura das palavras está incorreta")
        self.assertListEqual(map_result["doc6"][3], ["Meu","teste","de","palavras","."], "A leitura do texto está incorreto")

        '''Testam o checkTag'''
        self.assertListEqual(map_result["doc5"][4], ["p"],"A leitura das tags está incorreta")
        self.assertListEqual(map_result["doc6"][4], ["head","body","p","p"],"A leitura das tags está incorreta")

        '''Testam charBased'''
        self.assertListEqual(map_result["doc4"][5],
        ["l","a","l","a","l","a",".","\n","M","e","u"," ","t","e","s","t","e"," ","t","e","m"," ",
         "t","r","e","s"," ","p","a","r","a","g","r","a","f","o","s",".","\n","E","s","s","e"," ",
         "é"," ","o"," ","ú","l","t","i","m","o"], "A leitura dos caracteres está incorreta")
        #print(str(map_result["doc5"][5]))
        self.assertListEqual(map_result["doc5"][5],
        ["O","l","a"," "," "," "," "," "," "," "," ",","," "," "," "," "," "," ","m","e","u"," ","n",
         "o","m","e"," ","é"," ","h","a","s","a","n","."], "A leitura dos caracteres está incorreta")
        self.assertListEqual(map_result["doc6"][5],
        ["M","e","u","t","e","s","t","e"," ","d","e"," ","p","a","l","a","v","r","a","s","."], "A leitura dos caracteres está incorreta")

class TestCaracterInterface(unittest.TestCase):

    def testGeral(self):

        arr_features = [WordTestFeature("ola feature", "Essa feature é divertitida",
                                         "SILVA Ola. Contando Olas. Conferencia dos Hello World",
                                         FeatureVisibilityEnum.public,
                                         FormatEnum.text_plain,
                                         FeatureTimePerDocumentEnum.MILLISECONDS),
                        SentenceTestFeature("outra feature legal", "Essa feature é divertitida",
                                         "SILVA Ola. Contando Olas. Conferencia dos Hello World",
                                         FeatureVisibilityEnum.public,
                                         FormatEnum.text_plain,
                                         FeatureTimePerDocumentEnum.MILLISECONDS),

                        ParagraphTestFeature("outra feature legal", "Essa feature é divertitida",
                                         "SILVA Ola. Contando Olas. Conferencia dos Hello World",
                                         FeatureVisibilityEnum.public,
                                         FormatEnum.text_plain,
                                         FeatureTimePerDocumentEnum.MILLISECONDS),

                        WordTestFeature("tag feature", "Essa feature é divertitida",
                                         "SILVA Ola. Contando Olas. Conferencia dos Hello World",
                                         FeatureVisibilityEnum.public,
                                         FormatEnum.HTML,
                                         FeatureTimePerDocumentEnum.MILLISECONDS),

                        TagTestFeature("tag legal feature", "Essa feature é divertitida",
                                         "SILVA Ola. Contando Olas. Conferencia dos Hello World",
                                         FeatureVisibilityEnum.public,
                                         FormatEnum.HTML,
                                         FeatureTimePerDocumentEnum.MILLISECONDS),
                        CharTestFeature("char legal feature", "Essa feature é divertitida",
                                         "SILVA Ola. Contando Olas. Conferencia dos Hello World",
                                         FeatureVisibilityEnum.public,
                                         FormatEnum.HTML,
                                         FeatureTimePerDocumentEnum.MILLISECONDS)
                        ]

        dataset = "feature/tests/datasetZipFile.zip"
        datasetfile = "feature/tests/resultDatasetFile.txt"
        datReader = DatasetDocReader(dataset)
        docWriter = DatasetDocWriter(datasetfile)
        FeatureCalculator.featureManager.computeFeatureSetDocuments(datReader,docWriter,arr_features,FormatEnum.text_plain)

        with open(datasetfile,"r") as file:
            result_textfile = json.loads(file.read())

        '''Exemplo para o teste unitario geral: gerar o resultado de todas as features em um arquivo cópia
            Ao executar o feature calculator, comparar o conteúdo do arquivo de saída com o arquivo de cópia
            Assim todas as modificações serão testadas'''


        str_result = {"data": {"datasetZipFile/0012.txt": [["b", "'", "Oi", ",", "eu", "sou", "a", "Beatriz", "e", "estou", "fazendo", "o", "primeiro", "teste\\n", "'"], ["b'Oi, eu sou a Beatriz e estou fazendo o primeiro teste\\n'"], ["b'Oi, eu sou a Beatriz e estou fazendo o primeiro teste\\n'"], ["b", "'", "Oi", ",", "eu", "sou", "a", "Beatriz", "e", "estou", "fazendo", "o", "primeiro", "teste\\n", "'"], [], ["b", "'", "O", "i", ",", " ", "e", "u", " ", "s", "o", "u", " ", "a", " ", "B", "e", "a", "t", "r", "i", "z", " ", "e", " ", "e", "s", "t", "o", "u", " ", "f", "a", "z", "e", "n", "d", "o", " ", "o", " ", "p", "r", "i", "m", "e", "i", "r", "o", " ", "t", "e", "s", "t", "e", "\\", "n", "'"]], "datasetZipFile/0013.txt": [["b", "'", "Oi", ",", "eu", "sou", "a", "Beatriz", "e", "estou", "fazendo", "o", "segundo", "teste\\n", "'"], ["b'Oi, eu sou a Beatriz e estou fazendo o segundo teste\\n'"], ["b'Oi, eu sou a Beatriz e estou fazendo o segundo teste\\n'"], ["b", "'", "Oi", ",", "eu", "sou", "a", "Beatriz", "e", "estou", "fazendo", "o", "segundo", "teste\\n", "'"], [], ["b", "'", "O", "i", ",", " ", "e", "u", " ", "s", "o", "u", " ", "a", " ", "B", "e", "a", "t", "r", "i", "z", " ", "e", " ", "e", "s", "t", "o", "u", " ", "f", "a", "z", "e", "n", "d", "o", " ", "o", " ", "s", "e", "g", "u", "n", "d", "o", " ", "t", "e", "s", "t", "e", "\\", "n", "'"]], "datasetZipFile/": [["b", "'", "'"], ["b''"], ["b''"], ["b", "'", "'"], [], ["b", "'", "'"]], "datasetZipFile/0014.txt": [["b", "'", "Oi", ",", "eu", "sou", "a", "Beatriz", "e", "estou", "fazendo", "o", "ultimo", "e", "qualquer", "teste\\n", "'"], ["b'Oi, eu sou a Beatriz e estou fazendo o ultimo e qualquer teste\\n'"], ["b'Oi, eu sou a Beatriz e estou fazendo o ultimo e qualquer teste\\n'"], ["b", "'", "Oi", ",", "eu", "sou", "a", "Beatriz", "e", "estou", "fazendo", "o", "ultimo", "e", "qualquer", "teste\\n", "'"], [], ["b", "'", "O", "i", ",", " ", "e", "u", " ", "s", "o", "u", " ", "a", " ", "B", "e", "a", "t", "r", "i", "z", " ", "e", " ", "e", "s", "t", "o", "u", " ", "f", "a", "z", "e", "n", "d", "o", " ", "o", " ", "u", "l", "t", "i", "m", "o", " ", "e", " ", "q", "u", "a", "l", "q", "u", "e", "r", " ", "t", "e", "s", "t", "e", "\\", "n", "'"]]}, "header": {"0": {"params": "", "name": "ola feature"}, "1": {"params": "", "name": "outra feature legal"}, "2": {"params": "", "name": "outra feature legal"}, "3": {"params": "", "name": "tag feature"}, "4": {"params": "", "name": "tag legal feature"}, "5": {"params": "", "name": "char legal feature"}}}

        self.assertDictEqual(result_textfile,str_result,"O conteúdo dos textos não é igual")

        charinterface = CaracterInterface()
        charinterface.execute(dataset,datasetfile,arr_features,FormatEnum.text_plain)
        with open(datasetfile,"r") as file:
            result_textfile = json.loads(file.read())
        self.assertEqual(result_textfile,str_result,"O conteúdo dos textos não é igual")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'TestFeatureCalculator.testName']
    unittest.main()
