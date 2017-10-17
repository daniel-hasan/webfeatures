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
    
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super(TextBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)    
        self.int_sentences_counter = 0
    
    def checkSentence(self,document,sentence):
        self.int_sentences_counter = self.int_sentences_counter + 1
    
    def compute_feature(self):
        yield self.int_sentences_counter
        self.int_sentences_counter = 0

class LargeSentenceCountFeature(WordBasedFeature):
    '''
    Verifica a quantidade de frases grandes
    
    '''
    
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,int_size):
        super(WordBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)    
        self.int_size = int_size
        self.int_large_sentence = 0
        self.int_word_counter = 0
    
    def checkWord(self,document,word):
        if word in FeatureCalculator.sentence_divisors:
            large_sentence(int_word_counter)
        elif word not in FeatureCalculator.word_divisors:
            self.int_word_counter = self.int_word_counter + 1
            
    
    def large_sentence(int_sentence_size):
        if(int_sentence_size >= self.int_size):
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

                
class ParagraphCountFeature(ParagraphBasedFeature):
    '''
    Contabiliza o número de paragrafos de um texto
    
    '''
    
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super(TextBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)    
        self.int_paragraph_counter = 0
        
    def checkParagraph(self,document,paragraph):
        self.int_paragraph_counter = self.int_paragraph_counter + 1
    
    def compute_feature(self,document):
        yield self.int_paragraph_counter
        self.int_paragraph_counter = 0


class LargeParagraphCountFeature(WordBasedFeature):
    '''
    Contabiliza o número de paragrafos longos de um texto
    
    '''
    
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,size):
        super(WordBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)    
        self.int_large_paragraph = 0
        
    def checkWord(self,document,word):
        if word in FeatureCalculator.paragraph_divisors:
            int_large_paragraph(int_word_counter)
        elif word not in FeatureCalculator.word_divisors:
            self.int_word_counter = self.int_word_counter + 1
        
    def large_paragraph(self,int_paragraph_size):
        if(int_paragraph_size >= size):
            self.int_large_paragraph = self.int_large_paragraph + 1
    
    def compute_feature(self,document):
        yield self.int_large_paragraph
        self.int_large_paragraph = 0
