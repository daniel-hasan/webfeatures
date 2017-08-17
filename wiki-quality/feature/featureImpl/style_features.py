# -*- coding: utf-8 -*-
'''
Created on 8 de ago de 2017
Features de estrutura (como numero de seções, citações etc.)
@author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>  
'''
from feature import TextBasedFeature, WordBasedFeature




class SentenceCountFeature(TextBasedFeature):
    '''
    Contabiliza o número de frases de um texto
    '''
    pass

class WordCountFeature(WordBasedFeature):
    '''
    Contabiliza a ocorrencia de uma determinada lista de palavras
    Parametros:
    setWordsToCount: Lista representando as palavras a serem contabilizadas
    '''
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,setWordsToCount=set([])):
        super(WordBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)    
        self.setWordsToCount = set(setWordsToCount)


class LargeSentenceCountFeature(WordCountFeature):
    '''
    Contabiliza o número de frases grandes em um texto
    
    '''
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,int_phrase_size):
        super(WordCountFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)    
        self.int_phrase_size = int_phrase_size
                
class ParagraphCountFeature(TextBasedFeature):
    '''
    Contabiliza o número de paragrafos de um texto
    
    '''
    pass