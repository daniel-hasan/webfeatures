# -*- coding: utf-8 -*-
'''
Created on 8 de ago de 2017
Features de estrutura (como numero de seções, citações etc.)
@author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>  
'''

from abc import abstractmethod
from enum import Enum
import html
from statistics import stdev

from feature.featureImpl.style_features import WordCountFeature, \
    SentenceCountFeature, CharacterCountFeature
from feature.features import TagBasedFeature, WordBasedFeature, \
    SentenceBasedFeature, CharBasedFeature, FeatureVisibilityEnum
from utils.basic_entities import FormatEnum, FeatureTimePerDocumentEnum


class Proportional(Enum):
    WORD_COUNT = 1
    CHAR_COUNT = 2
    SENTENCE_COUNT = 3
    SECTION_COUNT = 4
    SUBSECTION_COUNT = 4
    @classmethod
    def get_enum(self,int_val):
        for enumFeat in Proportional:
            if(enumFeat.value == int_val):
                return enumFeat
        return None
    
    def get_feature(self):
        self.objFeature = None
        if(self == Proportional.WORD_COUNT):
            return WordCountFeature("Word Count","Word Count.",
                        "",
                        FeatureVisibilityEnum.public, 
                        FormatEnum.text_plain,FeatureTimePerDocumentEnum.MICROSECONDS,[],False)
        elif(self == Proportional.CHAR_COUNT):
            return CharacterCountFeature("Char Count","Char Count.",
                                            "",
                                            FeatureVisibilityEnum.public, 
                                            FormatEnum.text_plain,FeatureTimePerDocumentEnum.MICROSECONDS)
        elif(self == Proportional.SENTENCE_COUNT):
            return SentenceCountFeature("Sentence Count","Sentence Count.",
                        "",
                        FeatureVisibilityEnum.public, 
                        FormatEnum.text_plain,FeatureTimePerDocumentEnum.MICROSECONDS,[],False)
        elif(self == Proportional.SECTION_COUNT):
            return TagCountFeature("contagem de tags", "Feature que conta tags em HTML", "HTML", 
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.HTML, 
                                         FeatureTimePerDocumentEnum.MILLISECONDS,["h1"])
        elif(self == Proportional.SUBSECTION_COUNT):
            return TagCountFeature("contagem de tags", "Feature que conta tags em HTML", "HTML", 
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.HTML, 
                                         FeatureTimePerDocumentEnum.MILLISECONDS,["h2"])    
        return None
class TagCountFeature(TagBasedFeature,WordBasedFeature,SentenceBasedFeature,CharBasedFeature):
    
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,setTagsToCount=None,intPropotionalTo=None):
        super(TagBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)    
        if(setTagsToCount==None):
            setTagsToCount = []
        self.setTagsToCount = set([tag.lower() for tag in setTagsToCount])
        self.int_tag_counter = 0
        self.objFeature = None
        #adicionando o param intPropotionalTo como atributos (para serem gravadas no bd)
        self.intPropotionalTo = intPropotionalTo
        
        if(intPropotionalTo!=None):
            self.enumProportional = Proportional.get_enum(intPropotionalTo) 
            self.objFeature = self.enumProportional.get_feature()

    
    def startTag(self,document,tag,attrs,ignoreCount=False):
    
        if not ignoreCount and tag.lower() in self.setTagsToCount:
            self.int_tag_counter = self.int_tag_counter + 1
            
        if(self.objFeature != None and isinstance(self.objFeature,TagBasedFeature)):
            self.objFeature.startTag(document,tag,attrs)
        return True
            
              
    def compute_feature(self, document):
        intNorm = None
        if(self.objFeature != None):
            intNorm = self.objFeature.compute_feature(document)
        return self.int_tag_counter/intNorm if intNorm != None and intNorm != 0 else self.int_tag_counter
    
    def finish_document(self,document):
        self.int_tag_counter = 0
        if(self.objFeature!=None):
            self.objFeature.finish_document(document)
        
    #### Tag based Feature overide #########
    def data(self,document,str_data):
        if(self.objFeature != None and self.intPropotionalTo == Proportional.SECTION_COUNT.value):
            self.objFeature.data(document,str_data)
            return True
        return False
            
    def endTag(self,document,tag):
        if(self.objFeature != None  and self.intPropotionalTo == Proportional.SECTION_COUNT.value):
            self.objFeature.endTag(document,tag)
            return True
        return False
    
        
        
    #### WordBasedFeature,CharBasedFeature,SentenceBasedFeature overide #########
    def checkWord(self, document, word):
        if(self.objFeature != None and self.intPropotionalTo == Proportional.WORD_COUNT.value):
            self.objFeature.checkWord(document,word)
            
    def checkSentence(self, document, word):
        if(self.objFeature != None and self.intPropotionalTo == Proportional.SENTENCE_COUNT.value):
            self.objFeature.checkWord(document,word)
            
            
    def checkChar(self, document, word):
        if(self.objFeature != None and self.intPropotionalTo == Proportional.CHAR_COUNT.value): #isinstance(self.objFeature,CharBasedFeature)):
            self.objFeature.checkChar(document,word)
            return True
        else:
            return False
    
    
class LinkCountFeature(TagCountFeature):
    
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,bolExternal,bolInternalSameDomain,bolInternalSamePage,intPropotionalTo=None):
        super().__init__(name,description,reference,visibility,text_format,feature_time_per_document,setTagsToCount=["a"],intPropotionalTo=intPropotionalTo)    
        
        """adicionando os params booleanos como atributos (para serem gravados no bd)"""
        self.bolExternal=bolExternal
        self.bolInternalSameDomain=bolInternalSameDomain
        self.bolInternalSamePage=bolInternalSamePage
        self.intPropotionalTo = intPropotionalTo
        #if(self.name=="Same page link Count" or "Complete URL link Count"):
        #    print("Name: "+self.name+"\t external: "+str(self.bolExternal)+"\tsamedomain:"+str(self.bolInternalSameDomain)+"\t samepage: "+str(self.bolInternalSamePage))
    def startTag(self,document,tag,attrs):
        str_href = ""
        for att in attrs:
            if(att[0].lower() == "href"):
                str_href = att[1]
            
        if str_href == "" or str_href == None:
            super().startTag(document, tag, attrs,ignoreCount=True)
            return
        
        str_href = str_href.strip()
        bolIsExternal = str_href.startswith("http://") or str_href.startswith("https://")
        bolIsSamePage = str_href.startswith("#")
        bolIsSameDomain = not bolIsExternal and not bolIsSamePage
        count = (bolIsExternal and self.bolExternal) or \
                (bolIsSamePage and self.bolInternalSamePage) or \
                (bolIsSameDomain and self.bolInternalSameDomain)
        
        super().startTag(document, tag, attrs,ignoreCount=not count)
        return True
    
        

        

        
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
        return True
                
            
                            

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
        return True
    
    def data(self,document,str_data):
        #print("\tdados: "+str_data)
        if(self.bolReadingSection):
            self.sectionSize += len(html.unescape(str_data))
            #print("\t\tTamanho '"+str_data+"':"+str(len(str_data)))
            #print("\t\tTamanho atual:"+str(self.sectionSize))
        return True
    
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
        
        return stdev(self.arrSectionSizes) if len(self.arrSectionSizes) > 1 else 0
    
    def finish_document(self,document):
        self.arrSectionSizes=[]
        super().finish_document(document)
    