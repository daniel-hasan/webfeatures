# -*- coding: utf-8 -*-
class TextPreprocessing(object):
    def __init__(self,arr_preproc_methods):
        self.arr_preproc_methods = arr_preproc_methods
        
    def preprocess(self,strText):
        for objMethod in self.arr_preproc_methods:
            strText = objMethod.run(strText)
        return strText
    
class PreprocessingMethod(object):
    def run(self,text):
        pass
    
class StopWordRemoval(PreprocessingMethod):
    def run(self,text):
        pass
  
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
    
    