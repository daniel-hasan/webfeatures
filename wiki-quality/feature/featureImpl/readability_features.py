from feature.featureImpl.style_features import *
from feature.features import *
from utils.basic_entities import FeatureTimePerDocumentEnum, FormatEnum
from cmath import sqrt

class ReadabilityBasedFeature(CharBasedFeature, WordBasedFeature, SentenceBasedFeature):
    
    CHARCOUNT = "charCountFeature"
    WORDCOUNT = "wordCountFeature"
    SENTENCECOUNT = "sentenceCountFeature"
    SYLLABLECOUNT = "syllableCountFeature"
    COMPLEXWORDCOUNT = "complexWordCountFeature"
    POLYSYLLABLESCOUNT = "polysyllableCountFeature"
    ARR_FEATS_IN_CACHE = [CHARCOUNT,WORDCOUNT,SENTENCECOUNT,SYLLABLECOUNT,COMPLEXWORDCOUNT,POLYSYLLABLESCOUNT]
    
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document, arr_features_to_compute):
        super().__init__(name,description,reference,visibility,text_format,feature_time_per_document) 
        self.arr_feat_to_compute = set(arr_features_to_compute)
        
        self.charCountFeat = CharacterCountFeature("Char Count","Count the number of characters in the text.","reference",
                    FeatureVisibilityEnum.public, FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS, ignore_punctuation=True)
        
        self.wordCountFeat = WordCountFeature("Word Count","Count the number of words in the text.","reference",
                    FeatureVisibilityEnum.public, FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS,ignore_punctuation=True)
        
        self.syllableCountFeat = SyllableCountFeature("Syllable Count","Count the number of syllables in the text.","reference",
                                                      FeatureVisibilityEnum.public, FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS)
        
        self.complexWordCountFeat = WordsSyllablesCountFeature("Complex Word Count","Count the number of complex words in the text.","reference",
                    FeatureVisibilityEnum.public, FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS, 3)
        
        self.polysyllableCountFeat = WordsSyllablesCountFeature("Polysyllable Word Count","Count the number of polysyllables in the text.","reference",
                    FeatureVisibilityEnum.public, FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS, 4)
        
        self.sentenceCountFeat = SentenceCountFeature("Sentence Count","Count the number of sentences in the text.","reference",
                    FeatureVisibilityEnum.public, FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS)
    
    def checkChar(self, document, char):
        try:
            if ReadabilityBasedFeature.CHARCOUNT in self.arr_feat_to_compute:
                objCharCount = document.obj_cache.setCacheItem(ReadabilityBasedFeature.CHARCOUNT,self.charCountFeat,self)
                
                objCharCount.checkChar(document,char)
            
        except (NotTheOwner):
            pass
        
    def checkWord(self, document, word):
        try:
            if ReadabilityBasedFeature.WORDCOUNT in self.arr_feat_to_compute:
                objWordCount = document.obj_cache.setCacheItem(ReadabilityBasedFeature.WORDCOUNT,self.wordCountFeat,self)
                
                objWordCount.checkWord(document,word)
        
        except (NotTheOwner):
            pass
        
        try:
            if ReadabilityBasedFeature.SYLLABLECOUNT in self.arr_feat_to_compute:
                objWordCount = document.obj_cache.setCacheItem(ReadabilityBasedFeature.SYLLABLECOUNT,self.syllableCountFeat,self)
                
                objWordCount.checkWord(document,word)
                
        except (NotTheOwner):
            pass
        
        try:
            if ReadabilityBasedFeature.COMPLEXWORDCOUNT in self.arr_feat_to_compute:
                objWordCount = document.obj_cache.setCacheItem(ReadabilityBasedFeature.COMPLEXWORDCOUNT,self.complexWordCountFeat,self)
                objWordCount.checkWord(document,word)
            
        except (NotTheOwner):
            pass
        
        try:
            if ReadabilityBasedFeature.POLYSYLLABLESCOUNT in self.arr_feat_to_compute:
                objWordCount = document.obj_cache.setCacheItem(ReadabilityBasedFeature.POLYSYLLABLESCOUNT,self.polysyllableCountFeat,self)
                
                objWordCount.checkWord(document,word)
            
            
        except (NotTheOwner):
            pass
    
    def checkSentence(self, document, sentence):
        try:
            if ReadabilityBasedFeature.SENTENCECOUNT in self.arr_feat_to_compute:
                objSentenceCount = document.obj_cache.setCacheItem(ReadabilityBasedFeature.SENTENCECOUNT,self.sentenceCountFeat,self)
                
                objSentenceCount.checkSentence(document,sentence)
            
        except (NotTheOwner):
            pass
    
    @abstractmethod
    def compute_feature(self,document):
        raise NotImplementedError
 
    def finish_document(self, document):
        for strCacheValue in ReadabilityBasedFeature.ARR_FEATS_IN_CACHE:
            objFeatItem = document.obj_cache.getCacheItem(strCacheValue)
            if(objFeatItem != None):
                objFeatItem.finish_document(document)

    
class ARIFeature(ReadabilityBasedFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super().__init__(name,description,reference,visibility,text_format,feature_time_per_document,
        [ReadabilityBasedFeature.CHARCOUNT, ReadabilityBasedFeature.WORDCOUNT, ReadabilityBasedFeature.SENTENCECOUNT])    
    
    def compute_feature(self, document):
        objCharCount = document.obj_cache.getCacheItem(ReadabilityBasedFeature.CHARCOUNT)
        objWordCount = document.obj_cache.getCacheItem(ReadabilityBasedFeature.WORDCOUNT)
        objSentenceCount = document.obj_cache.getCacheItem(ReadabilityBasedFeature.SENTENCECOUNT)
        
        charCount = objCharCount.compute_feature(document)
        wordCount = objWordCount.compute_feature(document)
        sentenceCount = objSentenceCount.compute_feature(document)
        
        return 4.71*(charCount/wordCount) + 0.5*(wordCount/sentenceCount) - 21.42
    
    
class WFCountFeature(WordBasedFeature):
    ''' Contabiliza a média de frases a cada 100 palavras '''
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
    
    def finish_document(self, document):
        self.int_wf = 0
        self.int_word_counter = 0
        self.int_sentence_counter = 0
      
class ColemanLiauFeature(ReadabilityBasedFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super().__init__(name,description,reference,visibility,text_format,feature_time_per_document,
        [ReadabilityBasedFeature.CHARCOUNT,ReadabilityBasedFeature.WORDCOUNT])
        self.objwf = WFCountFeature("WF Count","Count the average of sentences in each fragment of 100 words in the text.","reference",
                                    FeatureVisibilityEnum.public, FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS)
    
    def checkWord(self, document, word):
        super().checkWord(document, word)
        self.objwf.checkWord(document, word)
        
    def compute_feature(self, document):
        
        objCharCount = document.obj_cache.getCacheItem(ReadabilityBasedFeature.CHARCOUNT)
        objWordCount = document.obj_cache.getCacheItem(ReadabilityBasedFeature.WORDCOUNT)
        charCount = objCharCount.compute_feature(document)
        wordCount = objWordCount.compute_feature(document)
        int_wf = self.objwf.compute_feature(document)
        return 5.89*(charCount/wordCount) + 0.3*int_wf - 15.48


class FleschReadingEaseFeature(ReadabilityBasedFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super().__init__(name,description,reference,visibility,text_format,feature_time_per_document,
        [ReadabilityBasedFeature.WORDCOUNT,ReadabilityBasedFeature.SENTENCECOUNT,ReadabilityBasedFeature.SYLLABLECOUNT])
    
    def compute_feature(self, document):
        objWordCount = document.obj_cache.getCacheItem(ReadabilityBasedFeature.WORDCOUNT)
        objSentenceCount = document.obj_cache.getCacheItem(ReadabilityBasedFeature.SENTENCECOUNT)
        objSyllableCount = document.obj_cache.getCacheItem(ReadabilityBasedFeature.SYLLABLECOUNT)
        wordCount = objWordCount.compute_feature(document)
        sentenceCount = objSentenceCount.compute_feature(document)
        syllableCount = objSyllableCount.compute_feature(document)
        
        return 206.835 - 1.015*(wordCount/sentenceCount) - 84.6*(syllableCount/wordCount)


class FleschKincaidFeature(ReadabilityBasedFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super().__init__(name,description,reference,visibility,text_format,feature_time_per_document,
        [ReadabilityBasedFeature.WORDCOUNT,ReadabilityBasedFeature.SENTENCECOUNT,ReadabilityBasedFeature.SYLLABLECOUNT]) 
        
    def compute_feature(self, document):
        objWordCount = document.obj_cache.getCacheItem(ReadabilityBasedFeature.WORDCOUNT)
        objSentenceCount = document.obj_cache.getCacheItem(ReadabilityBasedFeature.SENTENCECOUNT)
        objSyllableCount = document.obj_cache.getCacheItem(ReadabilityBasedFeature.SYLLABLECOUNT)
        wordCount = objWordCount.compute_feature(document)
        sentenceCount = objSentenceCount.compute_feature(document)
        syllableCount = objSyllableCount.compute_feature(document)
        
        return 0.39*(wordCount/sentenceCount) + 11.8*(syllableCount/wordCount) - 15.59
    

class GunningFogIndexFeature(ReadabilityBasedFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super().__init__(name,description,reference,visibility,text_format,feature_time_per_document,
        [ReadabilityBasedFeature.WORDCOUNT,ReadabilityBasedFeature.SENTENCECOUNT,ReadabilityBasedFeature.COMPLEXWORDCOUNT])       
    
    def compute_feature(self, document):
        objWordCount = document.obj_cache.getCacheItem(ReadabilityBasedFeature.WORDCOUNT)
        objSentenceCount = document.obj_cache.getCacheItem(ReadabilityBasedFeature.SENTENCECOUNT)
        objComplexWordCount = document.obj_cache.getCacheItem(ReadabilityBasedFeature.COMPLEXWORDCOUNT)
        wordCount = objWordCount.compute_feature(document)
        sentenceCount = objSentenceCount.compute_feature(document)
        complexWordCount = objComplexWordCount.compute_feature(document)
            
        return 0.4*(wordCount/sentenceCount + 100*(complexWordCount/wordCount))


class LasbarhetsindexFeature(ReadabilityBasedFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super().__init__(name,description,reference,visibility,text_format,feature_time_per_document,
        [ReadabilityBasedFeature.WORDCOUNT,ReadabilityBasedFeature.SENTENCECOUNT,ReadabilityBasedFeature.COMPLEXWORDCOUNT])    
         
    def compute_feature(self, document):
        objWordCount = document.obj_cache.getCacheItem(ReadabilityBasedFeature.WORDCOUNT)
        objSentenceCount = document.obj_cache.getCacheItem(ReadabilityBasedFeature.SENTENCECOUNT)
        objComplexWordCount = document.obj_cache.getCacheItem(ReadabilityBasedFeature.COMPLEXWORDCOUNT)
        wordCount = objWordCount.compute_feature(document)
        sentenceCount = objSentenceCount.compute_feature(document)
        complexWordCount = objComplexWordCount.compute_feature(document)
    
        return wordCount/sentenceCount + 100*(complexWordCount/wordCount)
    
class SmogGradingFeature(ReadabilityBasedFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super().__init__(name,description,reference,visibility,text_format,feature_time_per_document,
        [ReadabilityBasedFeature.POLYSYLLABLESCOUNT])    
         
    def compute_feature(self, document):
        objPolysyllableCount = document.obj_cache.getCacheItem(ReadabilityBasedFeature.WORDCOUNT)
        polysyllableCount = objPolysyllableCount.compute_feature(document)
    
        return 3 + sqrt(polysyllableCount)