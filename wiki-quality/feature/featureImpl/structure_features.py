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

from feature.features import TagBasedFeature, WordBasedFeature, \
    SentenceBasedFeature, CharBasedFeature


class TypeOfLink(enum):
    all_links=1
    just_external=2
    just_internal=3
    
class TagCountFeature(TagBasedFeature):
    
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,setTagsToCount=None):
        super(TagBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)    
        if(setTagsToCount==None):
            setTagsToCount = []
        self.setTagsToCount = set([tag.lower() for tag in setTagsToCount])
        self.int_tag_counter = 0
        
    
    
    def startTag(self,document,tag,attrs):
        if tag.lower() in self.setTagsToCount:
            self.int_tag_counter = self.int_tag_counter + 1
  
    def compute_feature(self, document):
        aux = self.int_tag_counter
        self.int_tag_counter = 0
        return aux

class LinkCountFeature(TagCountFeature):
    
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,typeOfLink):
        super().__init__(name,description,reference,visibility,text_format,feature_time_per_document,setTagsToCount=["a"])    
        self.typeOfLink = typeOfLink
        
    def startTag(self,document,tag,attrs):
        if("href" not in attrs):
            return
        
        count = (self.typeOfLink == TypeOfLink.just_external and (attrs["href"].startswith("http://")) or (attrs["href"].startswith("https://"))) or self.typeOfLink == TypeOfLink.just_internal 
        
        if count or self.typeOfLink == TypeOfLink.all_links:
            super().startTag(document, tag, attrs)
  
    
class TagCountFeaturePerFeature(TagCountFeature,WordBasedFeature,CharBasedFeature,SentenceBasedFeature):
    '''
    Created on 20 de fev de 2018
    Ratio between a tag count feature (current object) and another feature (another object)
    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>  
    '''
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,objFeature,setTagsToCount=None):
        super().__init__(name,description,reference,visibility,text_format,feature_time_per_document,setTagsToCount)
        self.objFeature = objFeature
    
    #### Tag based Feature overide #########
    def startTag(self,document,tag,attrs):
        super().startTag(document,tag,attrs)
        if(isinstance(self.objFeature,TagBasedFeature)):
            self.objFeature.startTag(document,tag,attrs)
    
    def data(self,document,str_data):
        super().data(document,str_data)
        if(isinstance(self.objFeature,TagBasedFeature)):
            self.objFeature.data(document,str_data)
            
    def endTag(self,document,tag):
        super().endTag(document,tag)
        if(isinstance(self.objFeature,TagBasedFeature)):
            self.objFeature.endTag(document,tag)
    
    def compute_feature(self, document):
        int_val_cur_obj =super().compute_feature(document)
        int_val_attr = self.objFeature.compute_feature(document) 
        return int_val_cur_obj/int_val_attr
    
    #### WordBasedFeature,CharBasedFeature,SentenceBasedFeature overide #########
    def checkWord(self, document, word):
        if(isinstance(self.objFeature,WordBasedFeature)):
            self.objFeature.checkWord(document,word)
    
    def checkSentence(self, document, word):
        if(isinstance(self.objFeature,SentenceBasedFeature)):
            self.objFeature.checkWord(document,word)
            
            
    def checkChar(self, document, word):
        if(isinstance(self.objFeature,CharBasedFeature)):
            self.objFeature.checkChar(document,word)            
        

        
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
        aux = self.intSumSizes/self.intNumSection if self.intNumSection!=0 else 0 
        self.intSumSizes = 0
        self.intNumSection = 0
        return aux
class LargestSectionSize(SectionSizeFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,intSectionLevel):
        super().__init__(name,description,reference,visibility,text_format,feature_time_per_document,intSectionLevel)
        self.intLargestSection = 0
    
    def lastSectionSize(self,intSectionSize):
        if(self.intLargestSection < intSectionSize):
            self.intLargestSection =intSectionSize
    
    def compute_feature(self, document):
        super().compute_feature(document)
        aux = self.intLargestSection
        self.intLargestSection = 0
        return aux
    
class ShortestSectionSize(SectionSizeFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,intSectionLevel):
        super().__init__(name,description,reference,visibility,text_format,feature_time_per_document,intSectionLevel)
        self.intShortestSection = float("inf")
    
    def lastSectionSize(self,intSectionSize):
        if(self.intShortestSection > intSectionSize):
            self.intShortestSection =intSectionSize
    
    def compute_feature(self, document):
        super().compute_feature(document)
        aux = self.intShortestSection if self.intShortestSection != float("inf") else 0
        self.intShortestSection = float("inf")
        return aux    
    
class StdDeviationSectionSize(SectionSizeFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,intSectionLevel):
        super().__init__(name,description,reference,visibility,text_format,feature_time_per_document,intSectionLevel)
        self.arrSectionSizes = []
    
    def lastSectionSize(self,intSectionSize):
        self.arrSectionSizes.append(intSectionSize)
    
    def compute_feature(self, document):
        super().compute_feature(document)
        stdevResult = stdev(self.arrSectionSizes) if len(self.arrSectionSizes) != 0 else 0
        self.arrSectionSizes=[]
        return stdevResult
    
    