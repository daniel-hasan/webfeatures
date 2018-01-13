# -*- coding: utf-8 -*-
'''
Created on 8 de ago de 2017
Features de estrutura (como numero de seções, citações etc.)
@author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>  
'''

from feature.features import *

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