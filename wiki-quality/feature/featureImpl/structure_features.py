# -*- coding: utf-8 -*-
'''
Created on 8 de ago de 2017
Features de estrutura (como numero de seções, citações etc.)
@author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>  
'''

from abc import abstractmethod
import enum
import html
from statistics import stdev

from feature.featureImpl.style_features import WordCountFeature, \
    SentenceCountFeature, CharacterCountFeature
from feature.features import TagBasedFeature, WordBasedFeature, \
    SentenceBasedFeature, CharBasedFeature, FeatureVisibilityEnum
from utils.basic_entities import FormatEnum, FeatureTimePerDocumentEnum

class Proportional(enum):
    WORD_COUNT = 1
    CHAR_COUNT = 2
    SENTENCE_COUNT = 3
    SECTION_COUNT = 4
    
    @classmethod
    def get_enum(int_val):
        for enum in Proportional:
            if(enum.value == int_val):
                return enum
        return None
    
    def get_feature(self):
        self.objFeature = None
        if(self == Proportional.WORD_COUNT):
            self.objFeature = WordCountFeature("Word Count","Word Count.",
                        "",
                        FeatureVisibilityEnum.public, 
                        FormatEnum.text_plain,FeatureTimePerDocumentEnum.MICROSECONDS,[],False)
        elif(self == Proportional.CHAR_COUNT):
            self.value = CharacterCountFeature("Char Count","Char Count.",
                                            "",
                                            FeatureVisibilityEnum.public, 
                                            FormatEnum.text_plain,FeatureTimePerDocumentEnum.MICROSECONDS,[],False)
        elif(self == Proportional.SENTENCE_COUNT):
            self.value = SentenceCountFeature("Sentence Count","Sentence Count.",
                        "",
                        FeatureVisibilityEnum.public, 
                        FormatEnum.text_plain,FeatureTimePerDocumentEnum.MICROSECONDS,[],False)
        elif(self == Proportional.SECTION_COUNT):
            self.value = TagCountFeature("contagem de tags", "Feature que conta tags em HTML", "HTML", 
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.HTML, 
                                         FeatureTimePerDocumentEnum.MILLISECONDS,["h1"])
        return None
class TagCountFeature(TagBasedFeature):
    
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,setTagsToCount=None,intPropotionalTo=None):
        super(TagBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)    
        if(setTagsToCount==None):
            setTagsToCount = []
        self.setTagsToCount = set([tag.lower() for tag in setTagsToCount])
        self.int_tag_counter = 0
        
        if(intPropotionalTo!=None):
            self.enumProportional = Proportional.get_enum(intPropotionalTo)
            self.objFeature = self.enum.get_feature()
    
    
    def startTag(self,document,tag,attrs):
        if tag.lower() in self.setTagsToCount:
            self.int_tag_counter = self.int_tag_counter + 1
            
        if(self.objFeature != None and isinstance(self.objFeature,TagBasedFeature)):
            self.objFeature.startTag(document,tag,attrs)  
    def compute_feature(self, document):
        intNorm = None
        if(self.objFeature != None):
            intNorm = self.objFeature.compute_feature(document)
        return self.int_tag_counter/intNorm if intNorm != None else self.int_tag_counter
    
    def finish_document(self,document):
        self.int_tag_counter = 0
        if(self.objFeature!=None):
            self.finish_document(document)
        
    #### Tag based Feature overide #########
    def data(self,document,str_data):
        if(self.objFeature != None and isinstance(self.objFeature,TagBasedFeature)):
            self.objFeature.data(document,str_data)
            
    def endTag(self,document,tag):
        if(self.objFeature != None and isinstance(self.objFeature,TagBasedFeature)):
            self.objFeature.endTag(document,tag)
    
    
        
        
    #### WordBasedFeature,CharBasedFeature,SentenceBasedFeature overide #########
    def checkWord(self, document, word):
        if(self.objFeature != None and isinstance(self.objFeature,WordBasedFeature)):
            self.objFeature.checkWord(document,word)
    
    def checkSentence(self, document, word):
        if(self.objFeature != None and isinstance(self.objFeature,SentenceBasedFeature)):
            self.objFeature.checkWord(document,word)
            
            
    def checkChar(self, document, word):
        if(self.objFeature != None and isinstance(self.objFeature,CharBasedFeature)):
            self.objFeature.checkChar(document,word)
    
    
    
class LinkCountFeature(TagCountFeature):
    
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,bolExternal,bolInternalSameDomain,bolInternalSamePage):
        super().__init__(name,description,reference,visibility,text_format,feature_time_per_document,setTagsToCount=["a"])    
        self.bolExternal = bolExternal
        self.bolInternalSameDomain = bolInternalSameDomain
        self.bolInternalSamePage = bolInternalSamePage
    
    def startTag(self,document,tag,attrs):
        if("href" not in attrs or attrs["href"] == None):
            return
        
        strHref = attrs["href"].strip 
        count = (self.bolExternal and (strHref.startswith("http://")) or (strHref.startswith("https://")))
        count = count or (self.bolInternalSamePage  and (strHref.startswith("#"))) or self.bolInternalSameDomain  
        
        if count:
            super().startTag(document, tag, attrs)
  
    
        

        

        
class SectionSizeFeature(TagBasedFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,intSectionLevel):
        super(TagBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)
        self.intSectionLevel = intSectionLevel
        self.strTagToRead = "h"+str(intSectionLevel)
        self.bolReadingSection = False
        self.sectionSize = 0
    
    def isSectionTag(self,tag):
        return (tag.startswith("h") or tag.startswith("H")) and len(tag) == 2 and tag[1].isdigit()
    
    def getSectionLevel(self,tag):
        return int(tag[1])
    
    @abstractmethod
    def lastSectionSize(self,intSectionSize):
        raise NotImplementedError  
      
    def sectionFinished(self):
        self.lastSectionSize(self.sectionSize)
        self.sectionSize = 0
        self.bolReadingSection = False
        
    """
    startTag finaliza a leitura seção, se necessario
    """ 
    def startTag(self,document,tag,attrs):
        #print("Inicia tag: "+tag)
        #se nao estiver dentro de uma secao, ao ler uma tag, verifica
        if(self.isSectionTag(tag)):
            
            intCurrentLevel = self.getSectionLevel(tag)


            #se estiver lendo a tag e for <= ao nivel que queremos, finalizar a tag
            if(self.bolReadingSection and intCurrentLevel<=self.intSectionLevel):
                #print("Terminou a seção!")
                self.sectionFinished()

                
            
                            

    """
    endtag inicializa a leitura seção, se necessario
    """     
    def endTag(self,document,tag):
        #print("Termina tag: "+tag)
        #se nao estiver lendo tag, e for igual ao nivel que queremos, começar a ler uma nova seção
        if(self.isSectionTag(tag)):
            intCurrentLevel = self.getSectionLevel(tag)
            if(not self.bolReadingSection and intCurrentLevel==self.intSectionLevel):
                self.bolReadingSection = True
                #print("Começou a ler a seção!")
    
    def data(self,document,str_data):
        #print("\tdados: "+str_data)
        if(self.bolReadingSection):
            self.sectionSize += len(html.unescape(str_data))
            #print("\t\tTamanho '"+str_data+"':"+str(len(str_data)))
            #print("\t\tTamanho atual:"+str(self.sectionSize))
            
    def compute_feature(self, document):
        if(self.bolReadingSection):
            #print("Terminou a seção!")
            self.sectionFinished()
        return 0
    
    def finish_document(self,document):
        pass
        
class AverageSectionSize(SectionSizeFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,intSectionLevel):
        super().__init__(name,description,reference,visibility,text_format,feature_time_per_document,intSectionLevel)
        self.intSumSizes = 0
        self.intNumSection = 0
    def lastSectionSize(self,intSectionSize):
        self.intSumSizes =  self.intSumSizes+intSectionSize
        self.intNumSection = self.intNumSection + 1
        #print("Seção tamanho: "+str(intSectionSize))
        
    def compute_feature(self, document):
        super().compute_feature(document)

        return self.intSumSizes/self.intNumSection if self.intNumSection!=0 else 0
    
    def finish_document(self,document):
        self.intSumSizes = 0
        self.intNumSection = 0
        super().finish_document(document)
        
class LargestSectionSize(SectionSizeFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,intSectionLevel):
        super().__init__(name,description,reference,visibility,text_format,feature_time_per_document,intSectionLevel)
        self.intLargestSection = 0
    
    def lastSectionSize(self,intSectionSize):
        if(self.intLargestSection < intSectionSize):
            self.intLargestSection =intSectionSize
    
    def compute_feature(self, document):
        super().compute_feature(document)
        return self.intLargestSection
    
    def finish_document(self,document):
        self.intLargestSection = 0
        super().finish_document(document)
        
class ShortestSectionSize(SectionSizeFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,intSectionLevel):
        super().__init__(name,description,reference,visibility,text_format,feature_time_per_document,intSectionLevel)
        self.intShortestSection = float("inf")
    
    def lastSectionSize(self,intSectionSize):
        if(self.intShortestSection > intSectionSize):
            self.intShortestSection =intSectionSize
    
    def compute_feature(self, document):
        super().compute_feature(document)
        
        return self.intShortestSection if self.intShortestSection != float("inf") else 0    
    
    def finish_document(self,document):
        self.intShortestSection = float("inf")
        super().finish_document(document)
        
class StdDeviationSectionSize(SectionSizeFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,intSectionLevel):
        super().__init__(name,description,reference,visibility,text_format,feature_time_per_document,intSectionLevel)
        self.arrSectionSizes = []
    
    def lastSectionSize(self,intSectionSize):
        self.arrSectionSizes.append(intSectionSize)
    
    def compute_feature(self, document):
        super().compute_feature(document)
        
        return stdev(self.arrSectionSizes) if len(self.arrSectionSizes) != 0 else 0
    
    def finish_document(self,document):
        self.arrSectionSizes=[]
        super().finish_document(document)
    