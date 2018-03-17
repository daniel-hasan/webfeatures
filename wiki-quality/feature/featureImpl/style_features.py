# -*- coding: utf-8 -*-
'''
Created on 8 de ago de 2017
Features de estrutura (como numero de seções, citações etc.)
@author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>  
'''

from statistics import mean

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
        return True
    def compute_feature(self, document):
        return self.int_sentences_counter
    
    def finish_document(self,document):
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
            self.large_sentence(self.int_word_counter)
            
        elif word not in FeatureCalculator.word_divisors:
            self.int_word_counter = self.int_word_counter + 1
        return True
    def large_sentence(self,int_sentence_size):
        if(int_sentence_size >= self.int_size):
            self.int_large_sentence = self.int_large_sentence + 1
            self.int_word_counter = 0
    
    def compute_feature(self, document):
        return self.int_large_sentence
    
    def finish_document(self,document):
        self.int_large_sentence = 0
        self.int_word_counter = 0
        
class LargeSentenceSizeFeature(WordBasedFeature):
    '''
    Retorna o tamanho da maior frase
    '''
    
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super(WordBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)    
        self.int_large_sentence = 0
        self.int_word_counter = 0
    
    def checkWord(self,document,word):
        if word in FeatureCalculator.sentence_divisors:
            self.large_sentence(self.int_word_counter)
            
        elif word not in FeatureCalculator.word_divisors:
            self.int_word_counter = self.int_word_counter + 1
        return True 
    def large_sentence(self,int_sentence_size):
        if(int_sentence_size >= self.int_large_sentence):
            self.int_large_sentence = int_sentence_size
            self.int_word_counter = 0
    
    def compute_feature(self, document):
        return self.int_large_sentence
    
    def finish_document(self,document):
        self.int_large_sentence = 0
        self.int_word_counter = 0
        

        
        
class WordCountFeature(WordBasedFeature):
    '''
    Contabiliza a ocorrencia de uma determinada lista de palavras
    Parametros:
    setWordsToCount: Lista representando as palavras a serem contabilizadas
    '''
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,setWordsToCount=None,case_sensitive=False,ignore_punctuation=False):
        super(WordBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)    
        if(setWordsToCount==None):
            setWordsToCount = []
        if(not case_sensitive):
            setWordsToCount = [word.lower() for word in setWordsToCount]
        
        self.case_sensitive = case_sensitive
        self.setWordsToCount = set(setWordsToCount)
        self.int_word_counter = 0
        self.ignore_punctuation = ignore_punctuation
    
     
    def checkWord(self,document,word):
        if(self.ignore_punctuation and word in FeatureCalculator.word_divisors):
            return True
        
        if len(self.setWordsToCount) ==0 or word in self.setWordsToCount or (not self.case_sensitive and word.lower() in self.setWordsToCount):
            self.int_word_counter = self.int_word_counter + 1
        return True
    def compute_feature(self,document):
        return self.int_word_counter
    def reset_counter(self):
        self.int_word_counter = 0
        
    def finish_document(self,document):
        self.reset_counter()

class PhraseRateMoreThanAvgFeature(SentenceBasedFeature,WordCountFeature):
    '''
    Contabiliza a proporção de frases maiores do que a media (menos o tamanho passado como parametro)
    
    '''
    
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,bolLarge,intSize):
        super().__init__(name,description,reference,visibility,text_format,feature_time_per_document)    
        
        self.arr_sentences = []
        self.bolLarge = bolLarge
        self.intSize = intSize
    

    def checkSentence(self,document,sentence):
        self.arr_sentences.append(self.int_word_counter)
        self.reset_counter()
        return True
    def compute_feature(self, document):
        int_count = 0
        avgSize = mean(self.arr_sentences)
        for size in self.arr_sentences:
            if((self.bolLarge and size >= (avgSize+self.intSize)) or (not self.bolLarge and size<=(avgSize-self.intSize))):
                int_count = int_count+1
        return int_count/len(self.arr_sentences) if len(self.arr_sentences)>0 else 0
    
    def finish_document(self,document):
        self.arr_sentences = []
        
        
class BeginningSentenceWordCountFeature(SentenceBasedFeature):
    '''
    Contabiliza a ocorrencia de uma determinada lista de palavras
    Parametros:
    setWordsToCount: Lista representando as palavras a serem contabilizadas
    '''
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,setWordsToCount=None,case_sensitive=False):
        super().__init__(name,description,reference,visibility,text_format,feature_time_per_document)    
        if(setWordsToCount==None):
            setWordsToCount = []
        if(not case_sensitive):
            setWordsToCount = [word.lower() for word in setWordsToCount]
        
        self.case_sensitive = case_sensitive
        self.setWordsToCount = set(setWordsToCount)
        self.int_word_counter = 0
    
     
    def checkSentence(self,document,sentence):
        #get the first sentence word
        word_divisors = FeatureCalculator.word_divisors
        word = ""
        pos = 0
        sentence = sentence.strip()
        if(len(sentence)<1):
            return True
        
        while(pos < len(sentence) and sentence[pos] not in word_divisors):
            word += sentence[pos]
            pos = pos + 1
        word = word.lower() if not self.case_sensitive else word
        
        #check if exists and count
        if word in self.setWordsToCount:
            self.int_word_counter = self.int_word_counter + 1
        return True
    def compute_feature(self,document):
        return self.int_word_counter
    
    def finish_document(self,document):
        self.int_word_counter = 0        
        
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
        return self.int_paragraph_counter
    
    def finish_document(self,document):
        self.int_paragraph_counter = 0


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
        return True
        
    def large_paragraph(self,int_paragraph_size):
        if(int_paragraph_size >= self.size):
            self.int_large_paragraph = self.int_large_paragraph + 1
            self.int_word_counter = 0
    
    def compute_feature(self,document):
        return self.int_large_paragraph
    
    def finish_document(self,document):
        self.int_large_paragraph = 0

class CharacterCountFeature(CharBasedFeature):
    
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document, ignore_punctuation=False):
        super(CharBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)    
        self.int_char_counter = 0
        self.ignore_punctuation = ignore_punctuation
    
    def checkChar(self, document, char):
        if self.ignore_punctuation is True and char in FeatureCalculator.word_divisors:
            return True
        self.int_char_counter = self.int_char_counter + 1
        return True
    
    def compute_feature(self,document):
        return self.int_char_counter
    
    def finish_document(self,document):
        self.int_char_counter = 0
        
class SyllableCountFeature(WordBasedFeature):
    
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super(WordBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)    
        self.int_syllable_counter = 0
    
    def checkWord(self, document, word):
        syllable = hyphenator.hyphenate_word(word)
        self.int_syllable_counter = self.int_syllable_counter + len(syllable)
        return True
    def compute_feature(self, document):
        return self.int_syllable_counter
    
    def finish_document(self,document):
        self.int_syllable_counter = 0

class WordsSyllablesCountFeature(WordBasedFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document, int_syllables):
        super(WordBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)    
        self.int_syllables = int_syllables
        self.int_complexword_counter = 0
    
    def checkWord(self, document, word):
        syllable = hyphenator.hyphenate_word(word)
        int_syllable_counter = len(syllable)
        
        if int_syllable_counter >= self.int_syllables:
            self.int_complexword_counter = self.int_complexword_counter + 1
        return True
    def compute_feature(self, document):
        return self.int_complexword_counter
    
    def finish_document(self,document):
        self.int_complexword_counter = 0