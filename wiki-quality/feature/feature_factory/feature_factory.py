# -*- coding: utf-8 -*-
'''
Created on 8 de ago de 2017

@author: hasan
'''
from abc import abstractmethod

from feature import ConfigurableParam, ParamTypeEnum
from feature.language_dependent_words.featureImpl.style_features import *
from feature.language_dependent_words.featureImpl.structure_features import *
from feature.features import  FeatureVisibilityEnum
from utils.basic_entities import FormatEnum, FeatureTimePerDocumentEnum
from django.contrib.sessions.backends import file


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
        
        arrFeatures = [TagCountFeature("Section h1 Count", "Count the number of HTML h1 sections in the text", "reference", 
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.HTML, 
                                         FeatureTimePerDocumentEnum.MILLISECONDS,["h1"])]
        
        featTagCount = TagCountFeature("Section p Count", "Count the number of HTML p sections in the text", "reference", 
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.HTML, 
                                         FeatureTimePerDocumentEnum.MILLISECONDS,["p"])
        
        arrFeatures.append(featTagCount)
        
        featTagCount = TagCountFeature("Section div Count", "Count the number of HTML div sections in the text", "reference", 
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.HTML, 
                                         FeatureTimePerDocumentEnum.MILLISECONDS,["div"])
        arrFeatures.append(featTagCount)
    
class StyleFeatureFactory(FeatureFactory):
    def createFeatures(self):
        '''
        Cria as features de estilo de escrita (numero de preposicoes, pronomes, etc).
        Parametros:
            language: objeto da classe utils.Language
        '''
        PosClassLang = self.class_language_dependent("PartOfSpeech")
        
        arrFeatures = []
        
        featSentenceCount = SentenceCountFeature("Phrase Count","Count the number of phrases in the text.","reference",
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS)
        
        featLargeSentenceCount = LargeSentenceCountFeature("Large Phrase Count","Count the number of phrases larger than a specified threshold.",
                                                           "reference",FeatureVisibilityEnum.public,FormatEnum.text_plain,
                                                           FeatureTimePerDocumentEnum.MICROSECONDS,10)
        
        featLargeSentenceCount.addConfigurableParam(ConfigurableParam("int_sentence_size","Sentence Size",
                                                                      "The sentence need to have (at least) this length (in words) in order to be considered a large phrase.",
                                                                      10,ParamTypeEnum.int))
        
        featParagraphCount = ParagraphCountFeature("Paragraph Count","Count the number of paragraph at text",
                                         "reference",
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS)
        
        featLargeParagraphCount = LargeParagraphCountFeature("Large Paragraph Count","Count the number of paragraphs larger than a specified threshold",
                                         "reference",
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS,16)
        
        featLargeSentenceCount.addConfigurableParam(ConfigurableParam("int_paragraph_size","Paragraph Size",
                                                                      "The paragraph need to have (at least) this length (in words) in order to be considered a large paragraph.",
                                                                      16,ParamTypeEnum.int))
        
        
        
        arrFeatures.append(featSentenceCount)
        arrFeatures.append(featLargeSentenceCount)
        arrFeatures.append(featParagraphCount)
        arrFeatures.append(featLargeParagraphCount)
        
        return  arrFeatures
        

class WordsFeatureFactory(FeatureFactory):
    
    def __init__(self,objLanguage):
        super(FeatureFactory,self).__init__()
        self.objLanguage = objLanguage
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.BASE_DIR = os.path.abspath(os.path.join(self.BASE_DIR,os.pardir))
        print(self.BASE_DIR)
    
    
    def getTestClasseGramatical(self, str_classe):
        
        fileClasseGramatical = self.BASE_DIR+"/partOfSpeech/"+self.objLanguage.name+"/" + str_classe + ".txt"
        with open(fileClasseGramatical) as file:
            listPrepositions = file.read().split(",")
        
        return listPrepositions
    
    def createFeatures(self):
        
        arrFeatures = []
        
        part_of_speech = ["articles","auxiliaryVerbs","coordinatingConjunctions","correlativeConjunctions",
                          "indefinitePronouns","interrogativePronouns","prepositions","pronouns",
                          "relativePronouns","subordinatingConjunctions","toBeVerbs"]
        
        for classe in part_of_speech:
            dirClasses = self.BASE_DIR + "/partOfSpeech/" + self.objLanguage.name + "/" + classe + ".txt"
            with open(dirClasses) as file:
                listWords = file.read().split(",")
                arrFeatures.append(WordBasedFeature(str(classe).title() + "Count","Count the number of "+ classe +" in the text.",
                                                 "Based on file style.c from path diction-1.11.tar.gz of http://ftp.gnu.org/gnu/diction/",
                                                 FeatureVisibilityEnum.public, 
                                                 FormatEnum.text_plain,FeatureTimePerDocumentEnum.MICROSECONDS,listWords))

        return arrFeatures