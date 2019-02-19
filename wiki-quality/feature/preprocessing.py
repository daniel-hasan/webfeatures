# -*- coding: utf-8 -*-
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class TextPreprocessing(object):
    def __init__(self,arr_preproc_methods):
        self.arr_preproc_methods = arr_preproc_methods
        
    def preprocess(self,strText):
        for objMethod in self.arr_preproc_methods:
            strText = objMethod.run(strText)
        return strText
    
class PreprocessingMethod(object):
    def run(self,text,language):
        pass
    
class StopWordRemoval(PreprocessingMethod):
    def run(self,text,language):
        str_stopword = set(stopwords.words(language))
        list_tokened_words = word_tokenize(text)
        list_filtered_text = [word for word in word_tokens if not w in stop_words]
        return str(" ".join(list_filtered_text))
  
class PartOfSpeechParser(PreprocessingMethod):
    def run(self,text):
        pass    
    
class DocumentSetPreprocessing(object):
    def run(self,strDirCollection):
        pass

class NumberOfDocumentCount(DocumentSetPreprocessing):
    def __init__(self):
        self.num_docs = 0
    def run(self,strDirCollection):
        '''
            Calcula o numero de documentos da colecao
        '''
        self.num_docs = 102#alterar para o numero calculado
        pass
    
    