# -*- coding: utf-8 -*-
'''
Created on 8 de ago de 2017
Features de estrutura (como numero de seções, citações etc.)
@author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>  
'''

from feature.features import * 


class SentenceCountFeature(SentenceBasedFeature):
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
    

class LargeSentenceCountFeature(WordBasedFeature):
    '''
    Verifica a quantidade de frases grandes
    '''
    
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,size):
        super(WordBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)    
        self.setWordsToCount = set(setWordsToCount)
    
    def checkWord(self,document,word):
        if word in FeatureCalculator.sentence_divisors:
            int_large_sentence(int_word_counter)
        elif word not in FeatureCalculator.word_divisors:
            self.int_word_counter = self.int_word_counter + 1
            
    
    def int_large_sentence(int_sentence_size):
        if(int_word_counter >= size):
            self.int_large_sentence = self.int_large_sentence + 1
    
    def compute_feature(self, document):
        yield self.int_large_sentence
        self.int_large_sentence = 0
        
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
    
    def compute_feature(self,document):
        yield self.int_word_counter
        self.int_word_counter = 0

                
class ParagraphCountFeature(TextBasedFeature):
    '''
    Contabiliza o número de paragrafos de um texto
    
    '''
    pass