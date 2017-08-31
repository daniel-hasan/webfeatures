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
    
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,setSentencesToCount=set([])):
        super(TextBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)    
        self.setSentencesToCount = set(setSentencesToCount) 
    
    
    def int_count_sentences(self):
        int_sentences = texto.split(".")
        int_sentences = len(int_words)
        return int_sentences
    

class WordCountFeature(WordBasedFeature):
    '''
    Contabiliza a ocorrencia de uma determinada lista de palavras
    Parametros:
    setWordsToCount: Lista representando as palavras a serem contabilizadas
    '''
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,setWordsToCount=set([])):
        super(WordBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)    
        self.setWordsToCount = set(setWordsToCount)
        self.int_word_counter = 0
        
    def checkWord(self,document,word):
        if word in self.setWordsToCount:
            self.int_word_counter = self.int_word_counter + 1
    
    def feature_result(self,document):
        int_aux = self.int_word_counter
        self.int_word_counter = 0        
        return int_aux

class LargeSentenceCountFeature(WordCountFeature):
    '''
    Contabiliza o número de frases grandes em um texto
    
    '''
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,int_phrase_size):
        super(WordCountFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)    
        self.int_phrase_size = int_phrase_size
    def bool_is_large(int_count_words, size):
        if(int_count_words < size)
              return False
        else
              return True
                
class ParagraphCountFeature(TextBasedFeature):
    '''
    Contabiliza o número de paragrafos de um texto
    
    '''
    pass