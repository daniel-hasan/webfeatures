from feature.featureImpl.style_features import *
from feature.features import *
from utils.basic_entities import FeatureTimePerDocumentEnum, FormatEnum
from math import sqrt

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

        self.arrWordFeatures = [self.wordCountFeat,self.syllableCountFeat,self.complexWordCountFeat,self.polysyllableCountFeat]
        self.arrWordFeatTypes= [ReadabilityBasedFeature.WORDCOUNT,ReadabilityBasedFeature.SYLLABLECOUNT,ReadabilityBasedFeature.COMPLEXWORDCOUNT, ReadabilityBasedFeature.POLYSYLLABLESCOUNT]
        self.initialize_cache_flags()
         
    def initialize_cache_flags(self):
        
        
        self.isFirstTimeChar = True
        self.isFirstTimeSentence = True
        
        self.isOwnerCheckChar = False
        self.isOwnerCheckSentence = False
            
    def hasToCompute(self,document,objFeature,strFeatType):
        if(strFeatType not in self.arr_feat_to_compute):
            return False
        try:
            document.obj_cache.setCacheItem(strFeatType,objFeature,self)
            return True
        except (NotTheOwner):
            return False
            
    
                
    def checkChar(self, document, char):
        if(self.isFirstTimeChar):
            self.isOwnerCheckChar = self.hasToCompute(document, self.charCountFeat, ReadabilityBasedFeature.CHARCOUNT)
            self.isFirstTimeChar = False
        if self.isOwnerCheckChar:
            self.charCountFeat.checkChar(document,char)
            return True
        return False
        
    def checkWord(self, document, word):
        
        bolIsCheckWord = False
        for i,objFeature in enumerate(self.arrWordFeatures):
            checkWord = self.hasToCompute(document, objFeature, self.arrWordFeatTypes[i])
                
            if(checkWord):
                objFeature.checkWord(document,word)
                bolIsCheckWord = True
        return bolIsCheckWord
    def checkSentence(self, document, sentence):
        
        if(self.isFirstTimeSentence):
            self.isOwnerCheckSentence = self.hasToCompute(document, self.sentenceCountFeat, ReadabilityBasedFeature.SENTENCECOUNT)
            self.isFirstTimeSentence = False
        if self.isOwnerCheckSentence:
            self.sentenceCountFeat.checkSentence(document,sentence)
            return True
        return False
    
    @abstractmethod
    def compute_feature(self,document):
        raise NotImplementedError
 
    def finish_document(self, document):
        self.initialize_cache_flags()
        
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
        if word in FeatureCalculator.sentence_divisors and self.int_word_counter < 100:
            self.int_sentence_counter = self.int_sentence_counter + 1
        
        elif self.int_word_counter == 100:
            self.int_wf = self.int_wf + 1
            self.int_word_counter = 0
            
        self.int_word_counter = self.int_word_counter + 1
    
    def compute_feature(self,document):
        if self.int_wf == 0:
            return self.int_sentence_counter
        
        return self.int_sentence_counter/self.int_wf
    
    def finish_document(self, document):
        self.int_wf = 0
        self.int_word_counter = 0
        self.int_sentence_counter = 0
      
class ColemanLiauFeature(ReadabilityBasedFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super().__init__(name,description,reference,visibility,text_format,feature_time_per_document,
        [ReadabilityBasedFeature.CHARCOUNT,ReadabilityBasedFeature.WORDCOUNT,ReadabilityBasedFeature.SENTENCECOUNT])
        self.objwf = WFCountFeature("WF Count","Count the average of sentences in each fragment of 100 words in the text.","reference",
                                    FeatureVisibilityEnum.public, FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS)
    
    def checkWord(self, document, word):
        super().checkWord(document, word)
        self.objwf.checkWord(document, word)
        return True
    def compute_feature(self, document):
        
        objCharCount = document.obj_cache.getCacheItem(ReadabilityBasedFeature.CHARCOUNT)
        objWordCount = document.obj_cache.getCacheItem(ReadabilityBasedFeature.WORDCOUNT)
        objSentenceCount = document.obj_cache.getCacheItem(ReadabilityBasedFeature.SENTENCECOUNT)
        charCount = objCharCount.compute_feature(document)
        wordCount = objWordCount.compute_feature(document)
        sentenceCount = objSentenceCount.compute_feature(document)
        int_wf = self.objwf.compute_feature(document)
        return 5.87*(charCount/wordCount) - 29.58*(sentenceCount/wordCount) - 15.80


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