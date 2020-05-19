# -*- coding: utf-8 -*-
'''
Created on 8 de ago de 2017

@author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
'''
from abc import abstractmethod
from enum import Enum
import html
from html.parser import HTMLParser
import os
from os.path import join, isfile, isdir
from os import listdir
import re

from utils.basic_entities import FormatEnum, CheckTime



class NotTheOwner(Exception):
    def __init__(self):
        super().__init__(self, "Object is not the owner: Permission denied or cache's empty")

class DocumentCache(object):

    def __init__(self,obj):
        self.cache = {}
        self.owner = {}

    def hasCacheItem(self, itemName):
        return itemName in self.cache

    def getCacheItem(self, itemName, objRequest=None):
        if itemName not in self.cache:
            return None
        if objRequest != None and self.owner[itemName] != objRequest:
            raise NotTheOwner()
        return self.cache[itemName]

    def setCacheItem(self, itemName, intValue, objRequest):
        if not self.hasCacheItem(itemName):
            self.setOwnership(itemName, objRequest)

        if self.owner[itemName] != objRequest:
            raise NotTheOwner()
        self.cache[itemName] = intValue
        return self.cache[itemName]

    def setOwnership(self, itemName, objRequest):
        self.owner[itemName] = objRequest

class Document(object):
    def __init__(self,int_doc_id,str_doc_name,str_text):
        self.int_doc_id = int_doc_id
        self.str_doc_name = str_doc_name
        self.str_text = str_text
        self.obj_cache = DocumentCache(self)

class FeatureDocumentsWriter(object):
    @abstractmethod
    def write_document(self,document, arr_feats_used, arr_feats_result):
        #raise NotImplementedError("Voce deve criar uma subclasse e a mesma deve sobrepor este método")
        pass

    @abstractmethod
    def write_header(self, arr_features_used):
        #raise NotImplementedError
        pass

    @abstractmethod
    def finishAllDocuments(self):
        #raise NotImplementedError
        pass

class FeatureDocumentsReader(object):
    '''
            Classe abstrata para a leitura dos textos
            de um conjunto de documentos. Implemente este
            leitor nos demais modulos para a leitura dos documentos.
            @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    '''
    @abstractmethod
    def get_documents(self):
        #raise NotImplementedError
        pass


class DocSetFileReader(FeatureDocumentsReader):
    def __init__(self,file):
        self.file = file

    '''
        Erro de função não encontrada
    '''

    def get_documents(self):
        int_count = 0
        for str_file in listdir(self.file):
            str_file_path = join(self.file, str_file)
            if isfile(str_file_path) and not isdir(str_file_path):
                with open(str_file) as file:
                    str_data = file.read()
                    yield Document(int_count, str_file,str_data)
                    int_count = int_count+1



class DocSetReaderDummy(FeatureDocumentsReader):
    def get_documents(self):
        yield Document(1,"doc1","Ola meu nome é hasan")
        yield Document(2,"doc2","ipi ipi ura")
        yield Document(3,"doc3","lalala")

#class FeatureClassToExtract(object):
#    def __init__(self,feature_class,arr_feature_arguments):
#        self.feature_class = feature_class
#        self.arr_feature_arguments = arr_feature_arguments

#    def instantiate_feature(self):
#        module = __import__( "feature" )
#        Klass = getattr(module,self.feature_class)
#        return Klass(**self.arr_feature_arguments)

class ParserTags(HTMLParser):
    def __init__(self, arrParserFeats, document):
        HTMLParser.__init__(self)
        self.document = document
        self.arrParserFeats = arrParserFeats


        self.firstTimeData = True
        self.firstTimeStartTag = True
        self.firstTimeEndTag = True
        self.arrFeatsStartTag = []
        self.arrFeatsEndTag = []
        self.arrFeatsData = []
    def handle_data(self,str_data):
        if(self.firstTimeData):
            self.arrFeatsData = [feat for feat in self.arrParserFeats if feat.data(self.document, str_data)]
            self.firstTimeData = False
        else:
            for feat in self.arrFeatsData:
                feat.data(self.document, str_data)

    def handle_starttag(self, tag, attrs):
        if(self.firstTimeStartTag):
            self.arrFeatsStartTag = [feat for feat in self.arrParserFeats if feat.startTag(self.document, tag, attrs)]
            self.firstTimeStartTag = False
        else:
            for feat in self.arrFeatsStartTag:
                feat.startTag(self.document, tag, attrs)

    def handle_endtag(self, tag):
        if(self.firstTimeEndTag):
            self.arrFeatsEndTag = [feat for feat in self.arrParserFeats if feat.endTag(self.document, tag)]
            self.firstTimeEndTag = False
        else:
            for feat in self.arrFeatsEndTag:
                feat.endTag(self.document, tag)
        #[feat.endTag(self.document, tag) for feat in self.arrParserFeats]
        #self.feat.endTag(self.document, tag)

class FeatureCalculatorManager(object):

    def computeFeatureSetDocuments(self,datReader,docWriter,arr_features_to_extract,format):
        '''
            a partir de um diretorio FeatureDocumentsReader extrai as features de todos os textos.
            arr_features_to_extract são implementações da classe Feature calculator
            devem ser tranformados em um array de features para chamar, para cada documento,
            o método computeFeatureSet.
            @author:
        '''
            #cria um array arr_features (array de FeatureCalculator)
            # com as features do array arr_features_to_extract

            # Rodar todos os docuemntos para todas as features que não
            # necessitam de algum metodo de preprocessamento de todo o conjunto de documento

        docWriter.write_header(arr_features_to_extract)

        for doc in datReader.get_documents():
            arr_features_result = self.computeFeatureSet(doc, arr_features_to_extract,format)
            #Para cada um processamento do documentSet necessário,
            # rodar todas as features que necessitam dele.
            docWriter.write_document(doc,arr_features_to_extract,arr_features_result)


        docWriter.finishAllDocuments()

    def reduce_array(self,arrToReduce,arrIdx):
            arrIdx.sort(reverse=True)
            for idx in arrIdx:
                del arrToReduce[idx]

    def computeFeatureSet(self,docText,arr_features,format):
        '''
        Analisa o texto e calcula todas as features do array.
        Primeiro é calculada as features do formato HTML, depois, textplain.

        [fazer depois a parte de preprocessamento] Para cada formato:  Agrupa o conjunto de fetures no tipo
        de preprocessamento do texto. Faz o preprocessamento roda as features para
        este determinado preprocessamento.

        Rode primeiramente todas as TextBasedFeature usando
        o texto completo e, logo apos, para cada palavra, rode todas as WordCountFeatures


        Saída: arranjo para cada posicao de arrFeature, a resposta da feture correspondente

        @author:
        '''


        str_text = docText.str_text
        arr_feat_result = []

        for feat in arr_features:
            arr_feat_result.append(None)
        str_text_for_char = str_text
        timeToProc = CheckTime()
        if format is FormatEnum.HTML:

            arrTagFeats = [feat for feat in arr_features if isinstance(feat, TagBasedFeature)]

            parser = ParserTags(arrTagFeats, docText)
            parser.feed(str_text)

            #timeToProc.printDelta("HTML parser tags")

            '''considera apenas o que estiver dentro de <body> </body> (se esses elementos existirem)'''
            str_text_lower = str_text.lower()
            int_pos_body = str_text_lower.find("<body>")
            int_pos_fim_body = str_text_lower.find("</body>")
            if(int_pos_body >=0 and int_pos_fim_body>=0):
                str_text = str_text[int_pos_body+6:int_pos_fim_body]
            '''str_text = parser.str_plain_text'''
            str_text_for_char = re.sub("<[^>]+>", "", str_text)
            str_text = re.sub("<[^>]+>", " ", str_text)

            '''elimina as html entities'''
            str_text = html.unescape(str_text)
            str_text_for_char = html.unescape(str_text_for_char)
            #timeToProc.printDelta("String parsing")

        #armazo as word based features e sentence based feature
        word_buffer = ""
        sentence_buffer = ""
        paragraph_buffer = ""

        #separa os tipos de features par a dar o check
        arrCharFeats = [feat for feat in arr_features if isinstance(feat, CharBasedFeature)]
        arrWordFeats = [feat for feat in arr_features if isinstance(feat, WordBasedFeature)]
        arrSentFeats = [feat for feat in arr_features if isinstance(feat, SentenceBasedFeature)]
        arrParFeats = [feat for feat in arr_features if isinstance(feat, ParagraphBasedFeature)]


        #timeToProc.printDelta("proc char feats")
        #print("Arr features size: "+str(len(arr_features))+" Char: "+str(len(arrCharFeats)))
        #t = 1
        for feat in arrCharFeats:
            for str_char_for_char in str_text_for_char:
                if not feat.checkChar(docText,str_char_for_char):
                    #print("Ignored: "+feat.name)
                    break
                #t = 1+t
                #if isinstance(feat, CharBasedFeature):
                #    xx = xx+1
                #if isinstance(feat, CharBasedFeature):
            #timeToProc.printDelta("Feature "+feat.name)

        #timeToProc.printDelta("Check char")
        firstTimeWord = True
        arrCheckWordIdxToRemove = []
        firstTimeSentence = True
        arrCheckSentIdxToRemove = []
        # Checagem de pontos das palavras
        #arrParagraphsPoints = []
        #arrSentencePoints =[]
        #arrWordsPoints = []
        #for i,str_char in enumerate(str_text):
        #    if(str_char in FeatureCalculator.word_divisors):
        #        arrWordsPoints.append(i)
        #    if(str_char in FeatureCalculator.sentence_divisors):
        #        arrSentencePoints.append(i)
        #    if(str_char in FeatureCalculator.paragraph_divisor):
        #        arrParagraphsPoints.append(i)
        #timeToProc.printDelta("Check word,sentence and paragraph points")
        #print("numchar: "+str(len(str_text))+" Num words: "+str(len(arrWordsPoints))+" NumSents: "+str(len(arrSentencePoints))+"Num Pars: "+str(len(arrParagraphsPoints)))


        for str_char in str_text:
            word_proc = word_buffer.strip()
            if(len(word_proc) > 0 and str_char in FeatureCalculator.word_divisors):
                for i,feat in enumerate(arrWordFeats):

                    if(firstTimeWord):
                        bolChecked = feat.checkWord(docText, word_proc)
                        if(not bolChecked):
                            arrCheckWordIdxToRemove.append(i)
                    else:
                        feat.checkWord(docText, word_proc)
                    if(str_char != " "):
                        feat.checkWord(docText, str_char)

                    word_buffer = ""
                if(firstTimeWord):
                    firstTimeWord = False
                    #lenWordFeats = len(arrWordFeats)
                    self.reduce_array(arrWordFeats, arrCheckWordIdxToRemove)
                    #print("Words reduced From: "+str(lenWordFeats)+ " to "+str(len(arrWordFeats)))

            else:
                word_buffer = word_buffer + str_char

            sentence_buffer = sentence_buffer + str_char
            if(str_char in FeatureCalculator.sentence_divisors):
                    for i,feat in enumerate(arrSentFeats):
                        if(firstTimeSentence):
                            bolCheck = feat.checkSentence(docText,sentence_buffer)
                            if(not bolCheck):
                                arrCheckSentIdxToRemove.append(i)
                        else:
                            feat.checkSentence(docText,sentence_buffer)
                    sentence_buffer = ""

                    if(firstTimeSentence):
                        firstTimeSentence = False
                        #lenSentFeats = len(arrSentFeats)
                        self.reduce_array(arrSentFeats, arrCheckSentIdxToRemove)
                        #print("sentences reduced From: "+str(lenSentFeats)+ " to "+str(len(arrSentFeats)))




            if(paragraph_buffer != "" and str_char in FeatureCalculator.paragraph_divisor):
                    for feat in arrParFeats:
                        feat.checkParagraph(docText,paragraph_buffer)
                    paragraph_buffer = ""
            else:
                    paragraph_buffer = paragraph_buffer + str_char

        #timeToProc.printDelta("Check word, paragraph and sentence")
        #timeToProc.printDelta("Other checks")
        #se necessario, le a ultima palavra/frase/paragrafo do buffer

        paragraph_buffer = paragraph_buffer.strip()
        word_buffer = word_buffer.strip()
        sentence_buffer = sentence_buffer.strip(" ")

        for feat in arr_features:
            if(len(word_buffer) > 0 and isinstance(feat, WordBasedFeature)):
                feat.checkWord(docText, word_buffer)

            if(len(sentence_buffer) > 0 and isinstance(feat, SentenceBasedFeature)):
                feat.checkSentence(docText, sentence_buffer)

            if(len(paragraph_buffer) > 0 and isinstance(feat, ParagraphBasedFeature)):
                feat.checkParagraph(docText, paragraph_buffer)
        #timeToProc.printDelta("Last  checking")
        #para todoas as WordBasedFeatue ou SentenceBased feature, rodar o compute_feature

        aux = 0
        for feat in arr_features:
            arr_feat_result[aux] = feat.compute_feature(docText)
            aux = aux + 1
        #timeToProc.printDelta("Compute feature")
        for feat in arr_features:
            feat.finish_document(docText)
        #timeToProc.printDelta("Finish document")

        return arr_feat_result

class FeatureVisibilityEnum(Enum):
    '''
        Enum responsável pela visibilidade das features
        @author:  Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    '''
    public = "Visibilidade total"
    local = "Visibilidade nas interfaces (web e de caracteres, por ex) apenas se for localhost"
    private = "Não serão visualizadas nas interfaces (web e de caracteres) apenas rodando na linha de comando"

class FeatureCalculator(object):
    '''
        Classe abstrata das features. Os demais módulos deverão acessar as
        features apenas por meio desta classe.
        @author:  Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    '''
    featureManager = FeatureCalculatorManager()
    word_divisors = set([" ",",",".","!","?",";","%","&","*","(",")","-","@","#","+","/","=","[","]","}","{","\n","|","\"","'"])
    sentence_divisors = set([".","!","?"])
    paragraph_divisor = set(["\n", os.linesep])

    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):

        self.name = name
        self.description = description
        self.reference = reference
        self.visibility = visibility
        self.text_format = text_format
        self.feature_time_per_document = feature_time_per_document
        self.arr_configurable_param = []

    def addConfigurableParam(self,objParam):
        self.arr_configurable_param.append(objParam)

    def get_params_str(self):
        arrParams = []
        for param in self.arr_configurable_param:
            if(param.att_name in self.__dict__):
                arrParams.append(param.name+":"+self.__dict__[param.att_name])

        return "; ".join(arrParams)
    @abstractmethod
    def compute_feature(self,document):
        raise NotImplementedError

    @abstractmethod
    def finish_document(self,document):
        raise NotImplementedError


class TextBasedFeature(FeatureCalculator):

    pass

class ParagraphBasedFeature(FeatureCalculator):

    @abstractmethod
    def checkParagraph(self,document,paragraph):
        raise NotImplementedError

class SentenceBasedFeature(FeatureCalculator):

    @abstractmethod
    def checkSentence(self,document,sentence):
        raise NotImplementedError

class WordBasedFeature(FeatureCalculator):

    @abstractmethod
    def checkWord(self,document,word):
        raise NotImplementedError


class TagBasedFeature(FeatureCalculator):

    def startTag(self,tag, attrs):
        return False

    def endTag(self,tag, attrs):
        return False

    def data(self,document,str_data):
        return False

class CharBasedFeature(FeatureCalculator):

    @abstractmethod
    def checkChar(self,document,char):
        raise NotImplementedError
class ParamTypeEnum(Enum):
    '''
        Tipo do valor de um parametro de uma feature.
        @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    '''
    int = "int"
    float = "float"
    string = "string"
    choices = "choices"

class ConfigurableParam(object):
    '''
        Classe que armazena os parametros de uma feature que são configuráveis pelo usuário.
        @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    '''
    def __init__(self,att_name,name,description,default_value,param_type,arr_choices=[]):
        self.name = name
        self.att_name = att_name
        self.description = description
        self.default_value = default_value
        self.param_type = param_type
        self.arr_choices = arr_choices

class GraphBasedFeature(FeatureCalculator):
        @abstractmethod
        def compute_feature(self,graph):
                pass
