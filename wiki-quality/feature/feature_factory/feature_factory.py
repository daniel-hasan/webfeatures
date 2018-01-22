# -*- coding: utf-8 -*-
'''
Created on 8 de ago de 2017

@author: hasan
'''
from abc import abstractmethod

from feature import ConfigurableParam, ParamTypeEnum
from feature.featureImpl import *
from feature.features import  FeatureVisibilityEnum
from utils.basic_entities import FormatEnum, FeatureTimePerDocumentEnum


class FeatureFactory(object):
    '''
    Cria as features de um determinado tipo.
    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>  
    '''  
    def class_language_dependent(self,str_class):
        '''
        resgata a classe com um vocabulario dependente de linguagem a ser usa
        @todo: Nem todos as linguas sao implementadas, deve-se lançar uma exceção e 
        assim não criar a feature caso nao encontre a classe
        ''' 
        module = __import__( "feature.feature_factory.language_dependent_words."+self.language.name+"_words" )
        Klass = getattr(module,str_class)
        return Klass
    
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
    def createFeatures(self):
        '''
        Cria as features de estilo de escrita (numero de preposicoes, pronomes, etc).
        Parametros:
            language: objeto da classe utils.Language
        '''
        PosClassLang = self.class_language_dependent("PartOfSpeech")
        arrFeatures = [WordCountFeature("Preposition Count","Count the number of prepositions in the text.",FeatureVisibilityEnum.public,
                                        FormatEnum.text_plain,FeatureTimePerDocumentEnum.MICROSECONDS,setWordsToCount=PosClassLang.PREPOSITION)]
        
        featSentenceCount = SentenceCountFeature("Phrases Count","Count the number of phrases in the text.","reference",
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS)
        
        featLargeSentenceCount = LargeSentenceCountFeature("Largest Phrases Count","Count the number of phrases larger than a specified threshold.",
                                                           "reference",FeatureVisibilityEnum.public,FormatEnum.text_plain,
                                                           FeatureTimePerDocumentEnum.MICROSECONDS,10)
        
        featLargeSentenceCount.addConfigurableParam(ConfigurableParam("int_sentence_size","Sentence Size",
                                                                      "The sentence need to have (at least) this length (in words) in order to be considered a large phrase.",
                                                                      10,ParamTypeEnum.int))
        
        featParagraphCount = ParagraphCountFeature("Paragraph Count","Count the number of paragraph at text",
                                         "reference",
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS)
        
        featLargeParagraphCount = LargeParagraphCountFeature("Largest Paragraph Count","Count the number of paragraphs larger than a specified threshold",
                                         "reference",
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS,16)
        
        featLargeSentenceCount.addConfigurableParam(ConfigurableParam("int_paragraph_size","Paragraph Size",
                                                                      "The paragraph need to have (at least) this length (in words) in order to be considered a large paragraph.",
                                                                      16,ParamTypeEnum.int))
        
        featTagCount = TagCountFeature("Tag Count", "Count the number of incidents of HTML tags passed by parameter in the text", "reference", 
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.HTML, 
                                         FeatureTimePerDocumentEnum.MILLISECONDS,["head","body"])
        
        arrFeatures.append(featSentenceCount)
        arrFeatures.append(featLargeSentenceCount)
        arrFeatures.append(featParagraphCount)
        arrFeatures.append(featLargeParagraphCount)
        arrFeatures.append(featTagCount)
        
        return  arrFeatures
        
