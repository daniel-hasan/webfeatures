# -*- coding: utf-8 -*-
'''
Created on 8 de ago de 2017
Features de estrutura (como numero de seções, citações etc.)
@author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>  
'''

from abc import abstractmethod

from feature.features import TagBasedFeature


class TagCountFeature(TagBasedFeature):
    
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,setTagsToCount=None):
        super(TagBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)    
        if(setTagsToCount==None):
            setTagsToCount = []
        self.setTagsToCount = set(setTagsToCount)
        self.int_tag_counter = 0
    
    def checkTag(self, document, tag):
        if tag in self.setTagsToCount:
            self.int_tag_counter = self.int_tag_counter + 1
  
    def compute_feature(self, document):
        aux = self.int_tag_counter
        self.int_tag_counter = 0
        return aux
    
class SectionSizeFeature(TagBasedFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,intSectionLevel):
        super(TagBasedFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)
        self.intSectionLevel = intSectionLevel
        self.strTagToRead = "h"+str(intSectionLevel)
        self.bolReadingSection = False
        self.bolFirstSection = True
        self.sectionSize = 0
    
    def isSectionTag(self,tag):
        return tag.startswith("h") and len(tag) == 2 and tag[1].isdigit()
    
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
        
        #se nao estiver dentro de uma secao, ao ler uma tag, verifica
        if(self.isSectionTag(tag)):
            intCurrentLevel = self.getSectionLevel(tag[1])


            #se estiver lendo a tag e for <= ao nivel que queremos, finalizar a tag
            if(self.bolReadingSection and intCurrentLevel<=self.intSectionLevel):
                self.sectionFinished()

                
            
                            
    def checkTag(self, document, tag):
        pass
    """
    endtag inicializa a leitura seção, se necessario
    """     
    def endTag(self,document,tag):
        #se nao estiver lendo tag, e for igual ao nivel que queremos, começar a ler uma nova seção
        if(self.isSectionTag(tag)):
            intCurrentLevel = self.getSectionLevel(tag[1])
            if(not self.bolReadingSection and intCurrentLevel==self.intSectionLevel):
                self.bolReadingSection = True
    
    def data(self,document,str_data):
        if(self.bolReadingSection):
            self.sectionSize += self.sectionSize+len(str_data)
            
    def compute_feature(self, document):
        if(self.bolReadingSection):
            self.sectionFinished()
        return 0
    
class AverageSectionSize(SectionSizeFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,intSectionLevel):
        super(SectionSizeFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document,intSectionLevel)
        self.intSumSizes = 0
        self.intNumSection = 0
    def lastSectionSize(self,intSectionSize):
        self.intSumSizes =  self.intSumSizes+intSectionSize
        self.intNumSection = self.intNumSection + 1
        
    def compute_feature(self, document):
        super(SectionSizeFeature,self).compute_feature(document)
        aux = self.intSumSizes/self.intNumSection if self.intNumSection!=0 else 0 
        self.intSumSizes = 0
        self.intNumSection = 0
        return aux
class LargestSectionSize(SectionSizeFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,intSectionLevel):
        super(SectionSizeFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document,intSectionLevel)
        self.intLargestSection = 0
    
    def lastSectionSize(self,intSectionSize):
        if(self.intLargestSection < intSectionSize):
            self.intLargestSection =intSectionSize
    
    def compute_feature(self, document):
        super(SectionSizeFeature,self).compute_feature(document)
        aux = self.intLargestSection
        self.intLargestSection = 0
        return aux
    
class ShortestSectionSize(SectionSizeFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,intSectionLevel):
        super(SectionSizeFeature,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document,intSectionLevel)
        self.intShortestSection = float("inf")
    
    def lastSectionSize(self,intSectionSize):
        if(self.intShortestSection > intSectionSize):
            self.intShortestSection =intSectionSize
    
    def compute_feature(self, document):
        super(SectionSizeFeature,self).compute_feature(document)
        aux = self.intShortestSection if self.intShortestSection != float("inf") else 0
        self.intShortestSection = float("inf")
        return aux    
    
