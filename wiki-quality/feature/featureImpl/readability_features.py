from feature.featureImpl.style_features import *
from feature.features import *
from utils.basic_entities import FeatureTimePerDocumentEnum, FormatEnum

class DocumentCache(object):
    
    def __init__(self,obj):
        self.cache = {"characterCount":0}
        self.owner = {"characterCount":obj}
    
    def hasCacheItem(self, nomeItem):
        return nomeItem in self.cache 

    def getCacheItem(self, itemName, objRequest=None):
        if objRequest != None and self.owner[itemName] != objRequest:
            raise NotTheOwner()
        return self.cache[itemName]

    def setCacheItem(self, itemName, intValue, objRequest):
        if self.owner[itemName] != objRequest:
            raise NotTheOwner()
        self.owner[itemName] = intValue
        

class NotTheOwner(Exception):
    pass

class ARIFeature(ReadabilityBasedFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super(ReadabilityBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)    
        self.char = DocumentCache(self)
        self.word = DocumentCache(self)
        self.sentence = DocumentCache(self)
        self.charCount = 0
        self.wordCount = 0
        self.sentenceCount = 0
    
    def calculate(self, document):
        if not self.char.hasCacheItem("characterCount"):
            self.char.setCacheItem("characterCount",
                                   CharacterCountFeature("Char Count","Count the number of characters in the text.","reference",
                                    FeatureVisibilityEnum.public, FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS),self)
        
        if not self.char.hasCacheItem("wordCount"):
            self.char.setCacheItem("wordCount",
                                   WordCountFeature("Word Count","Count the number of words in the text.","reference",
                                    FeatureVisibilityEnum.public, FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS),self)
        
        if not self.char.hasCacheItem("sentenceCount"):
            self.char.setCacheItem("sentenceCount",
                                   SentenceCountFeature("Sentence Count","Count the number of sentences in the text.","reference",
                                    FeatureVisibilityEnum.public, FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS),self)
        
        try:
            charCount = self.char.getCacheItem("characterCount",self)
            wordCount = self.word.getCacheItem("wordCount", self)
            sentenceCount = self.sentence.getCacheItem("sentenceCount", self)
            self.charCount = charCount.compute_feature(document)
            self.wordCount = wordCount.compute_feature(document)
            self.sentenceCount = sentenceCount.compute_feature(document)
        
        except (Exception):
            pass
    
        return 4.71*(self.charCount/self.wordCount) + 0.5*(self.wordCount/self.sentenceCount) - 21.42
    
    def compute_feature(self, document):
        aux = self.calculate(document)
        return aux

class WFCountFeature(WordBasedFeature):
    '''
    Contabiliza a média de frases a cada 100 palavras
    
    '''
    
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super(WordBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)    
        self.int_sentence_counter = 0
        self.int_word_counter = 0
        self.int_wf = 0
        
    def checkWord(self,document,word):
        if word in FeatureCalculator.sentence_divisors and self.int_word_counter <= 100:
            self.int_sentence_counter = self.int_sentence_counter + 1
        else:
            self.int_wf = self.int_wf + 1
            self.int_word_counter = 0
        
    def compute_feature(self,document):
        return self.int_sentence_counter/self.int_wf
        
      
class CLFeature(ReadabilityBasedFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super(ReadabilityBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)    
        self.char = DocumentCache(self)
        self.word = DocumentCache(self)
        self.charCount = 0
        self.wordCount = 0
        self.wfCount = 0
    
    def calculate(self, document):
        if not self.char.hasCacheItem("characterCount"):
            self.char.setCacheItem("characterCount",
                                   CharacterCountFeature("Char Count","Count the number of characters in the text.","reference",
                                    FeatureVisibilityEnum.public, FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS),self)
        
        if not self.char.hasCacheItem("wordCount"):
            self.char.setCacheItem("wordCount",
                                   WordCountFeature("Word Count","Count the number of words in the text.","reference",
                                    FeatureVisibilityEnum.public, FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS),self)
        
        try:
            charCount = self.char.getCacheItem("characterCount",self)
            wordCount = self.word.getCacheItem("wordCount", self)
            self.charCount = charCount.compute_feature(document)
            self.wordCount = wordCount.compute_feature(document)
        
        except (Exception):
            pass
        
        int_wf = WFCountFeature("WF Count","Count the average of sentences in each fragment of 100 words in the text.","reference",
                                    FeatureVisibilityEnum.public, FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS)
        
        
        return 5.89*(self.charCount/self.wordCount) + 0.3*int_wf - 15.48
    
    def compute_feature(self, document):
        aux = self.calculate(document)
        return aux

class FREFeature(ReadabilityBasedFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super(ReadabilityBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)    
        self.word = DocumentCache(self)
        self.sentence = DocumentCache(self)
        self.syllable = DocumentCache(self)
        self.wordCount = 0
        self.sentenceCount = 0
        self.syllableCount = 0
    
    def calculate(self, document):
        if not self.char.hasCacheItem("wordCount"):
            self.char.setCacheItem("wordCount",
                                   WordCountFeature("Word Count","Count the number of words in the text.","reference",
                                    FeatureVisibilityEnum.public, FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS),self)
        
        if not self.char.hasCacheItem("sentenceCount"):
            self.char.setCacheItem("sentenceCount",
                                   SentenceCountFeature("Sentence Count","Count the number of sentences in the text.","reference",
                                    FeatureVisibilityEnum.public, FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS),self)
        
        if not self.char.hasCacheItem("syllableCount"):
            self.char.setCacheItem("syllableCount",
                                   SyllableCountFeature("Syllable Count","Count the number of syllables in the text.","reference",
                                    FeatureVisibilityEnum.public, FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS),self)
        
        try:
            wordCount = self.word.getCacheItem("wordCount", self)
            sentenceCount = self.sentence.getCacheItem("sentenceCount", self)
            syllableCount = self.syllable.getCacheItem("syllableCount", self)
            self.wordCount = wordCount.compute_feature(document)
            self.sentenceCount = sentenceCount.compute_feature(document)
            self.syllableCount = syllableCount.compute_feature(document)
        
        except (Exception):
            pass
    
        return 206.835 - 1.015*(self.wordCount/self.sentenceCount) - 84.6*(self.syllableCount/self.wordCount)
    
    def compute_feature(self, document):
        aux = self.calculate(document)
        return aux

class FKFeature(ReadabilityBasedFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super(ReadabilityBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)    
        self.word = DocumentCache(self)
        self.sentence = DocumentCache(self)
        self.syllable = DocumentCache(self)
        self.wordCount = 0
        self.sentenceCount = 0
        self.syllableCount = 0
    
    def calculate(self, document):
        if not self.char.hasCacheItem("wordCount"):
            self.char.setCacheItem("wordCount",
                                   WordCountFeature("Word Count","Count the number of words in the text.","reference",
                                    FeatureVisibilityEnum.public, FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS),self)
        
        if not self.char.hasCacheItem("sentenceCount"):
            self.char.setCacheItem("sentenceCount",
                                   SentenceCountFeature("Sentence Count","Count the number of sentences in the text.","reference",
                                    FeatureVisibilityEnum.public, FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS),self)
        
        if not self.char.hasCacheItem("syllableCount"):
            self.char.setCacheItem("syllableCount",
                                   SyllableCountFeature("Syllable Count","Count the number of syllables in the text.","reference",
                                    FeatureVisibilityEnum.public, FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS),self)
        
        try:
            wordCount = self.word.getCacheItem("wordCount", self)
            sentenceCount = self.sentence.getCacheItem("sentenceCount", self)
            syllableCount = self.syllable.getCacheItem("syllableCount", self)
            self.wordCount = wordCount.compute_feature(document)
            self.sentenceCount = sentenceCount.compute_feature(document)
            self.syllableCount = syllableCount.compute_feature(document)
        
        except (Exception):
            pass
    
        return 0.39*(self.wordCount/self.sentenceCount) + 11.8*(self.syllableCount/self.wordCount) - 15.59
    
    def compute_feature(self, document):
        aux = self.calculate(document)
        return aux

class GFIFeature(ReadabilityBasedFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super(ReadabilityBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)    
        self.word = DocumentCache(self)
        self.sentence = DocumentCache(self)
        self.complexWord = DocumentCache(self)
        self.wordCount = 0
        self.sentenceCount = 0
        self.complexWordCount = 0
    
    def calculate(self, document):
        if not self.char.hasCacheItem("wordCount"):
            self.char.setCacheItem("wordCount",
                                   WordCountFeature("Word Count","Count the number of words in the text.","reference",
                                    FeatureVisibilityEnum.public, FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS),self)
        
        if not self.char.hasCacheItem("sentenceCount"):
            self.char.setCacheItem("sentenceCount",
                                   SentenceCountFeature("Sentence Count","Count the number of sentences in the text.","reference",
                                    FeatureVisibilityEnum.public, FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS),self)
        
        if not self.char.hasCacheItem("complexWordCount"):
            self.char.setCacheItem("complexWordCount",
                                   ComplexWordsCountFeature("Complex Word Count","Count the number of complex words in the text.","reference",
                                    FeatureVisibilityEnum.public, FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS),self)
        
        try:
            wordCount = self.word.getCacheItem("wordCount", self)
            sentenceCount = self.sentence.getCacheItem("sentenceCount", self)
            complexWordCount = self.comlplexWord.getCacheItem("complexWordCount", self)
            self.wordCount = wordCount.compute_feature(document)
            self.sentenceCount = sentenceCount.compute_feature(document)
            self.complexWordCount = complexWordCount.compute_feature(document)
        
        except (Exception):
            pass
    
        return 0.4*(self.wordCount/self.sentenceCount + 100*(self.complexWordCount/self.wordCount))
    
    def compute_feature(self, document):
        aux = self.calculate(document)
        return aux

class LIXFeature(ReadabilityBasedFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super(ReadabilityBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)    
        self.word = DocumentCache(self)
        self.sentence = DocumentCache(self)
        self.complexWord = DocumentCache(self)
        self.wordCount = 0
        self.sentenceCount = 0
        self.complexWordCount = 0
    
    def calculate(self, document):
        if not self.char.hasCacheItem("wordCount"):
            self.char.setCacheItem("wordCount",
                                   WordCountFeature("Word Count","Count the number of words in the text.","reference",
                                    FeatureVisibilityEnum.public, FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS),self)
        
        if not self.char.hasCacheItem("sentenceCount"):
            self.char.setCacheItem("sentenceCount",
                                   SentenceCountFeature("Sentence Count","Count the number of sentences in the text.","reference",
                                    FeatureVisibilityEnum.public, FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS),self)
        
        if not self.char.hasCacheItem("complexWordCount"):
            self.char.setCacheItem("complexWordCount",
                                   ComplexWordsCountFeature("Complex Word Count","Count the number of complex words in the text.","reference",
                                    FeatureVisibilityEnum.public, FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS),self)
        
        try:
            wordCount = self.word.getCacheItem("wordCount", self)
            sentenceCount = self.sentence.getCacheItem("sentenceCount", self)
            complexWordCount = self.comlplexWord.getCacheItem("complexWordCount", self)
            self.wordCount = wordCount.compute_feature(document)
            self.sentenceCount = sentenceCount.compute_feature(document)
            self.complexWordCount = complexWordCount.compute_feature(document)
        
        except (Exception):
            pass
    
        return self.wordCount/self.sentenceCount + 100*(self.complexWordCount/self.wordCount)
    
    def compute_feature(self, document):
        aux = self.calculate(document)
        return aux