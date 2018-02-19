# -*- coding: utf-8 -*-
'''
Created on 8 de ago de 2017
Features de estrutura (como numero de seções, citações etc.)
@author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>  
'''

from feature.features import *
from feature.hyphenate import *


class SentenceCountFeature(SentenceBasedFeature):
    '''
    Contabiliza o número de frases de um texto
    
    '''
    
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super(SentenceBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)    
        self.int_sentences_counter = 0
    
    def checkSentence(self,document,sentence):
        self.int_sentences_counter = self.int_sentences_counter + 1
    
    def compute_feature(self, document):
        aux = self.int_sentences_counter
        self.int_sentences_counter = 0
        return aux

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
            self.large_sentence(self.int_word_counter)
            
        elif word not in FeatureCalculator.word_divisors:
            self.int_word_counter = self.int_word_counter + 1
            
    def large_sentence(self,int_sentence_size):
        if(int_sentence_size >= self.int_size):
            self.int_large_sentence = self.int_large_sentence + 1
            self.int_word_counter = 0
    
    def compute_feature(self, document):
        aux =  self.int_large_sentence
        self.int_large_sentence = 0
        self.int_word_counter = 0
        return aux
        
class WordCountFeature(WordBasedFeature):
    '''
    Contabiliza a ocorrencia de uma determinada lista de palavras
    Parametros:
    setWordsToCount: Lista representando as palavras a serem contabilizadas
    '''
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,setWordsToCount=None,case_sensitive=False):
        super(WordBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)    
        if(setWordsToCount==None):
            setWordsToCount = []
        if(not case_sensitive):
            setWordsToCount = [word.lower() for word in setWordsToCount]
        
        self.case_sensitive = case_sensitive
        self.setWordsToCount = set(setWordsToCount)
        self.int_word_counter = 0
    
     
    def checkWord(self,document,word):
        if word in self.setWordsToCount or (not self.case_sensitive and word.lower() in self.setWordsToCount):
            self.int_word_counter = self.int_word_counter + 1
    
    def compute_feature(self,document):
        aux = self.int_word_counter
        self.int_word_counter = 0
        return aux
        
class ParagraphCountFeature(ParagraphBasedFeature):
    '''
    Contabiliza o número de paragrafos de um texto
    
    '''
    
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super(ParagraphBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)    
        self.int_paragraph_counter = 0
        
    def checkParagraph(self,document,paragraph):
        self.int_paragraph_counter = self.int_paragraph_counter + 1
    
    def compute_feature(self,document):
        aux =  self.int_paragraph_counter
        self.int_paragraph_counter = 0
        return aux


class LargeParagraphCountFeature(WordBasedFeature):
    '''
    Contabiliza o número de paragrafos longos de um texto
    
    '''
    
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,size):
        super(WordBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)    
        self.int_large_paragraph = 0
        self.int_word_counter = 0
        self.size = size
        
    def checkWord(self,document,word):
        if word in FeatureCalculator.paragraph_divisor:
            self.large_paragraph(self.int_word_counter)
        elif word not in FeatureCalculator.word_divisors:
            self.int_word_counter = self.int_word_counter + 1
        
    def large_paragraph(self,int_paragraph_size):
        if(int_paragraph_size >= self.size):
            self.int_large_paragraph = self.int_large_paragraph + 1
            self.int_word_counter = 0
    
    def compute_feature(self,document):
        aux = self.int_large_paragraph
        self.int_large_paragraph = 0
        return aux

class CharacterCountFeature(CharBasedFeature):
    
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super(CharBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)    
        self.int_char_counter = 0
    
    def checkChar(self, document, char):
        self.int_char_counter = self.int_char_counter + 1
    
    def comṕute_feature(self,document):
        aux = self.int_char_counter
        self.int_char_counter = 0
        return aux

class SyllableCountFeature(WordBasedFeature):
    
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super(WordBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)    
        self.int_syllable_counter = 0
        self.hyphenate = Hyphenator(None,None)
    
    def checkWord(self, document, word):
        syllable = self.hyphenate.hyphenate_word(word)
        self.int_syllable_counter = self.int_syllable_counter + len(syllable)
    
    def compute_feature(self, document):
        aux = self.int_syllable_counter
        self.int_syllable_counter = 0
        return aux

class ComplexWordsCountFeature(WordBasedFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super(WordBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)    
        self.int_complexword_counter = 0
        self.hyphenate = Hyphenator(None,None)
    
    def checkWord(self, document, word):
        syllable = self.hyphenate.hyphenate_word(word)
        int_syllable = self.int_syllable_counter + len(syllable)
        
        if int_syllable >=3:
            self.int_complexword_counter = self.int_complexword_counter + 1
    
    def compute_feature(self, document):
        aux = self.int_complexword_counter
        self.int_complexword_counter = 0
        return aux