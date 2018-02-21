from feature.featureImpl.style_features import *
from feature.features import *
from utils.basic_entities import FeatureTimePerDocumentEnum, FormatEnum

class ReadabilityBasedFeature(CharBasedFeature, WordBasedFeature, SentenceBasedFeature):
    
    CHARCOUNT = "charCountFeature"
    WORDCOUNT = "wordCountFeature"
    SENTENCECOUNT = "sentenceCountFeature"
    SYLLABLECOUNT = "syllableCountFeature"
    COMPLEXWORDCOUNT = "complexWordCountFeature"
    POLYSYLLABLESCOUNT = "polysyllableCountFeature"
    ARR_FEATS_IN_CACHE = [CHARCOUNT,WORDCOUNT,SENTENCECOUNT,SYLLABLECOUNT,COMPLEXWORDCOUNT,POLYSYLLABLESCOUNT]
    
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document, arr_features_to_compute):
        super(FeatureCalculator,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document) 
        self.arr_feat_to_compute = set(arr_features_to_compute)
     
    def checkChar(self, document, char):
        try:
            if ReadabilityBasedFeature.CHARCOUNT in self.arr_feat_to_compute:
                objCharCount = document.obj_cache.setCacheItem(ReadabilityBasedFeature.CHARCOUNT,
                    CharacterCountFeature("Char Count","Count the number of characters in the text.","reference",
                    FeatureVisibilityEnum.public, FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS),self)
                
                objCharCount.checkChar(document,char)
            
        except (NotTheOwner):
            pass
        
    def checkWord(self, document, word):
        try:
            if ReadabilityBasedFeature.WORDCOUNT in self.arr_feat_to_compute:
                objWordCount = document.obj_cache.setCacheItem(ReadabilityBasedFeature.WORDCOUNT,
                    WordCountFeature("Word Count","Count the number of words in the text.","reference",
                    FeatureVisibilityEnum.public, FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS),self)
                
                objWordCount.checkWord(document,word)
        
        except (NotTheOwner):
            pass
        
        try:
            if ReadabilityBasedFeature.SYLLABLECOUNT in self.arr_feat_to_compute:
                objWordCount = document.obj_cache.setCacheItem(ReadabilityBasedFeature.SYLLABLECOUNT,
                    SyllableCountFeature("Syllable Count","Count the number of syllables in the text.","reference",
                    FeatureVisibilityEnum.public, FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS),self)
                
                objWordCount.checkWord(document,word)
                
        except (NotTheOwner):
            pass
        
        try:
            if ReadabilityBasedFeature.COMPLEXWORDCOUNT in self.arr_feat_to_compute:
                objWordCount = document.obj_cache.setCacheItem(ReadabilityBasedFeature.COMPLEXWORDCOUNT,
                    WordsSyllablesCountFeature("Complex Word Count","Count the number of complex words in the text.","reference",
                    FeatureVisibilityEnum.public, FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS, 3),self)
                
                objWordCount.checkWord(document,word)
            
        except (NotTheOwner):
            pass
        
        try:
            if ReadabilityBasedFeature.POLYSYLLABLESCOUNT in self.arr_feat_to_compute:
                objWordCount = document.obj_cache.setCacheItem(ReadabilityBasedFeature.POLYSYLLABLESCOUNT,
                    WordsSyllablesCountFeature("Polysyllable Word Count","Count the number of polysyllables in the text.","reference",
                    FeatureVisibilityEnum.public, FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS, 4),self)
                
                objWordCount.checkWord(document,word)
            
            
        except (NotTheOwner):
            pass
    
    def checkSentence(self, document, sentence):
        try:
            if ReadabilityBasedFeature.SENTENCECOUNT in self.arr_feat_to_compute:
                objSentenceCount = document.obj_cache.setCacheItem("sentenceCount",
                    SentenceCountFeature("Sentence Count","Count the number of sentences in the text.","reference",
                    FeatureVisibilityEnum.public, FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS),self)
                
                objSentenceCount.checkSentence(document,sentence)
            
        except (NotTheOwner):
            pass
    
    @abstractmethod
    def compute_feature(self,document):
        raise NotImplementedError
 
    def finish_document(self, document):
        for strCacheValue in ReadabilityBasedFeature.ARR_FEATS_IN_CACHE:
            objFeatItem = document.getCacheItem(strCacheValue)
            if(objFeatItem != None):
                objFeatItem.finish_document(document)

    
class ARIFeature(ReadabilityBasedFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super(ReadabilityBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document,
        [ReadabilityBasedFeature.CHARCOUNT, ReadabilityBasedFeature.WORDCOUNT, ReadabilityBasedFeature.SENTENCECOUNT])    
    
    def compute_feature(self, document):
        objCharCount = document.getCacheItem(ReadabilityBasedFeature.CHARCOUNT)
        objWordCount = document.getCacheItem(ReadabilityBasedFeature.WORDCOUNT)
        objSentenceCount = document.getCacheItem(ReadabilityBasedFeature.SENTENCECOUNT)
        
        charCount = objCharCount.compute_feature(document)
        wordCount = objWordCount.compute_feature(document)
        sentenceCount = objSentenceCount.compute_feature(document)
        
        return 4.71*(charCount/wordCount) + 0.5*(wordCount/sentenceCount) - 21.42

class WFCountFeature(WordBasedFeature):
    '''Contabiliza a média de frases a cada 100 palavras'''
    
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super(WordBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document,
        [])    
        self.int_sentence_counter = 0
        self.int_word_counter = 0
        
    def checkWord(self,document,word):
        if word in FeatureCalculator.sentence_divisors and self.int_word_counter < 100:
            self.int_sentence_counter = self.int_sentence_counter + 1
            self.int_word_counter = self.int_word_counter + 1
        
    def compute_feature(self,document):
        aux_sent = self.int_sentence_counter
        self.int_sentence_counter = 0
        self.int_word_counter = 0
        return aux_sent
        
      
class ColemanLiauFeature(ReadabilityBasedFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super(ReadabilityBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document,
        [ReadabilityBasedFeature.CHARCOUNT,ReadabilityBasedFeature.WORDCOUNT])
        self.objwf = WFCountFeature("WF Count","Count the average of sentences in each fragment of 100 words in the text.","reference",
                                    FeatureVisibilityEnum.public, FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS)
    
    def checkWord(self, document, word):
        super().checkWord(self, document, word)
        self.objwf.checkWord(document, word)
        
    def compute_feature(self, document):
        
        objCharCount = document.getCacheItem(ReadabilityBasedFeature.CHARCOUNT,self)
        objWordCount = document.getCacheItem(ReadabilityBasedFeature.WORDCOUNT,self)
        charCount = objCharCount.compute_feature(document)
        wordCount = objWordCount.compute_feature(document)
        int_wf = self.objwf.compute_feature(document)
        return 5.89*(charCount/wordCount) + 0.3*int_wf - 15.48


class FleschReadingEaseFeature(WordBasedFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super(WordBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document,
        [ReadabilityBasedFeature.WORDCOUNT,ReadabilityBasedFeature.SENTENCECOUNT,ReadabilityBasedFeature.SYLLABLECOUNT])
    
    def compute_feature(self, document):
        objWordCount = document.getCacheItem(ReadabilityBasedFeature.WORDCOUNT,self)
        objSentenceCount = document.getCacheItem(ReadabilityBasedFeature.SENTENCECOUNT,self)
        objSyllableCount = document.getCacheItem(ReadabilityBasedFeature.SYLLABLECOUNT,self)
        wordCount = objWordCount.compute_feature(document)
        sentenceCount = objSentenceCount.compute_feature(document)
        syllableCount = objSyllableCount.compute_feature(document)
        
        return 206.835 - 1.015*(wordCount/sentenceCount) - 84.6*(syllableCount/wordCount)


class FleschKincaidFeature(WordBasedFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super(WordBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document,
        [ReadabilityBasedFeature.WORDCOUNT,ReadabilityBasedFeature.SENTENCECOUNT,ReadabilityBasedFeature.SYLLABLECOUNT]) 
        
    def compute_feature(self, document):
        objWordCount = document.getCacheItem(ReadabilityBasedFeature.WORDCOUNT,self)
        objSentenceCount = document.getCacheItem(ReadabilityBasedFeature.SENTENCECOUNT,self)
        objSyllableCount = document.getCacheItem(ReadabilityBasedFeature.SYLLABLECOUNT,self)
        wordCount = objWordCount.compute_feature(document)
        sentenceCount = objSentenceCount.compute_feature(document)
        syllableCount = objSyllableCount.compute_feature(document)
        
        return 0.39*(wordCount/sentenceCount) + 11.8*(syllableCount/wordCount) - 15.59
    

class GunningFogIndexFeature(WordBasedFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super(WordBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document,
        [ReadabilityBasedFeature.WORDCOUNT,ReadabilityBasedFeature.SENTENCECOUNT,ReadabilityBasedFeature.COMPLEXWORDCOUNT])       
    
    def compute_feature(self, document):
        objWordCount = self.word.getCacheItem(ReadabilityBasedFeature.WORDCOUNT,self)
        objSentenceCount = self.sentence.getCacheItem(ReadabilityBasedFeature.SENTENCECOUNT,self)
        objComplexWordCount = self.comlplexWord.getCacheItem(ReadabilityBasedFeature.COMPLEXWORDCOUNT,self)
        wordCount = objWordCount.compute_feature(document)
        sentenceCount = objSentenceCount.compute_feature(document)
        complexWordCount = objComplexWordCount.compute_feature(document)
            
        return 0.4*(wordCount/sentenceCount + 100*(complexWordCount/wordCount))


class LasbarhetsindexFeature(WordBasedFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super(WordBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document,
        [ReadabilityBasedFeature.WORDCOUNT,ReadabilityBasedFeature.SENTENCECOUNT,ReadabilityBasedFeature.COMPLEXWORDCOUNT])    
         
    def compute_feature(self, document):
        objWordCount = document.getCacheItem(ReadabilityBasedFeature.WORDCOUNT, self)
        objSentenceCount = document.getCacheItem(ReadabilityBasedFeature.SENTENCECOUNT, self)
        objComplexWordCount = document.getCacheItem(ReadabilityBasedFeature.COMPLEXWORDCOUNT, self)
        wordCount = objWordCount.compute_feature(document)
        sentenceCount = objSentenceCount.compute_feature(document)
        complexWordCount = objComplexWordCount.compute_feature(document)
    
        return wordCount/sentenceCount + 100*(complexWordCount/wordCount)