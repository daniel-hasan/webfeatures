# -*- coding: utf-8 -*-
'''
Created on 8 de ago de 2017

@author: hasan
'''
from abc import abstractmethod

from feature import ConfigurableParam, ParamType
from feature.featureImpl import WordCountFeature, \
    LargeSentenceCountFeature
from feature.features import Format, FeatureVisibility


class FeatureFactory(object):
    '''
    Cria as features de um determinado tipo.
    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>  
    '''  
     
    def class_language_dependent(self,str_class):
        '''
        resgata a classe com um vocabulario dependente de linguagem a ser usa
        @todo: Nem todos as linguas sao implementadas, deve-se lançar uma exceção e 
        assim não criar a feature
        ''' 
        module = __import__( "feature.feature_factory.language_dependent_words."+self.language.name+"_words" )
        Klass = getattr(module,self.feature_class)
        return Klass(**self.arr_feature_arguments)
    
    @abstractmethod
    def createFeatures(self):
        '''
            A implementação deste método deverá retornar uma lista
            de features. Demais módulos não poderão acessar as implementações 
            de features.
        '''
        raise NotImplemented
    
class StructureFeatureFactory(FeatureFactory):
    def createFeatures(self):
        pass
    
class StyleFeatureFactory(FeatureFactory):
    def createFeatures(self,language):
        '''
        Cria as features de estilo de escrita (numero de preposicoes, pronomes, etc).
        Parametros:
            language: objeto da classe utils.Language
        '''
        PosClassLang = self.class_language_dependent("PartOfSpeech")
        arrFeatures = [WordCountFeature("Preposition Count","Count the number of prepositions in the text",FeatureVisibility.public,Format.text_plain,setWordsToCount=PosClassLang.PREPOSITION)]
        
        featLargeSentenceCount = LargeSentenceCountFeature("Largest Phrase Count","Count the number of phrases larger than a specified threshold",FeatureVisibility.public,Format.text_plain,10)
        featLargeSentenceCount.addConfigurableParam(ConfigurableParam("int_phrase_size","Phrase Size",
                                                                      "The phrase need to have (at least) this length (in words) in order to be considered a large phrase",
                                                                      10,ParamType.int))
        arrFeatures.append(featLargeSentenceCount)
        
        return  arrFeatures
        
