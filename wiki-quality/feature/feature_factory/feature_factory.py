# -*- coding: utf-8 -*-
'''
Created on 8 de ago de 2017

@author: hasan
'''
from abc import abstractmethod

from feature import ConfigurableParam, ParamTypeEnum
from feature.featureImpl.style_features import *
from feature.featureImpl.structure_features import *
from feature.features import  FeatureVisibilityEnum
from utils.basic_entities import FormatEnum, FeatureTimePerDocumentEnum
from django.contrib.sessions.backends import file


class FeatureFactory(object):
    '''
    Cria as features de um determinado tipo.
    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>  
    '''  
    IS_LANGUAGE_DEPENDENT = False
    
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
        
        arrFeatures = [TagCountFeature("Section Count", "Count the number of sections (i.e. HTML h1 tags) in the text", "", 
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.HTML, 
                                         FeatureTimePerDocumentEnum.MILLISECONDS,["h1"]),
                       TagCountFeature("Subsection Count", "Count the number of subsections (i.e. HTML h1 tags) in the text", "", 
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.HTML, 
                                         FeatureTimePerDocumentEnum.MILLISECONDS,["h2"]),
                       LinkCountFeature("Complete URL link Count", "Count the number of  HTML 'a' tag in which the 'href' attribute refers to a complete URL.", "", 
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.HTML, 
                                         FeatureTimePerDocumentEnum.MILLISECONDS,["h2"],bolExternal=True,bolInternalSameDomain=False,bolInternalSamePage=False),
                       LinkCountFeature("Relative URL link Count", "Count the number of  HTML 'a' tag in which the 'href' attribute refers to a relative URL (e.g. /images/cow.gif).", "", 
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.HTML, 
                                         FeatureTimePerDocumentEnum.MILLISECONDS,["h2"],bolExternal=False,bolInternalSameDomain=True,bolInternalSamePage=False),
                       LinkCountFeature("Same page link Count", "Count the number of links which refers to some other elements in the same page."+
                                                                " In other words, count the number of HTML 'a' tags in which 'href' points to some html page id."+
                                                                " For example, the value '#mainDiv' point to an element in the page which the id is 'mainDiv'.", "", 
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.HTML, 
                                         FeatureTimePerDocumentEnum.MILLISECONDS,["h2"],bolExternal=False,bolInternalSameDomain=False,bolInternalSamePage=True),
                       AverageSectionSize("Mean section size","The ratio between the section size (in characters) and the section count","",
                                          FeatureVisibilityEnum.public, 
                                          FormatEnum.HTML, 
                                          FeatureTimePerDocumentEnum.MILLISECONDS,1
                                          ),
                       LargestSectionSize("Largest section size","The size (in characters) of the largest section.","",
                                          FeatureVisibilityEnum.public, 
                                          FormatEnum.HTML, 
                                          FeatureTimePerDocumentEnum.MILLISECONDS,1
                                          ),
                       ShortestSectionSize("Shortest section size","The size (in characters) of the shortest section","",
                                          FeatureVisibilityEnum.public, 
                                          FormatEnum.HTML, 
                                          FeatureTimePerDocumentEnum.MILLISECONDS,1
                                          ),                                              
                       StdDeviationSectionSize("Standard deviation of the section size","Standard deviation of the section size (in characters)","",
                                          FeatureVisibilityEnum.public, 
                                          FormatEnum.HTML, 
                                          FeatureTimePerDocumentEnum.MILLISECONDS,1
                                          ),

                       TagCountFeaturePerLengthFeature("Links per length","Number of links (considering the 'a' HTML tag) per length (in characters)","",
                                          FeatureVisibilityEnum.public, 
                                          FormatEnum.HTML, 
                                          FeatureTimePerDocumentEnum.MILLISECONDS,
                                          intCountLengthType=TagCountFeaturePerLengthFeature.CHAR_COUNT,intSectionLevel=None,setTagsToCount=["a"]
                                          ),
                        
                        TagCountFeaturePerLengthFeature("Links per section","The ratio between the number of links (considering the 'a' HTML tag) and the section count","",
                                          FeatureVisibilityEnum.public, 
                                          FormatEnum.HTML, 
                                          FeatureTimePerDocumentEnum.MILLISECONDS,
                                          intCountLengthType=TagCountFeaturePerLengthFeature.SECTION_COUNT,intSectionLevel=None,setTagsToCount=["a"]
                                          ),                       
                       
                        TagCountFeaturePerLengthFeature("Images per length","Number of images (considering the 'img' HTML tag) per length (in characters)","",
                                          FeatureVisibilityEnum.public, 
                                          FormatEnum.HTML, 
                                          FeatureTimePerDocumentEnum.MILLISECONDS,
                                          intCountLengthType=TagCountFeaturePerLengthFeature.CHAR_COUNT,intSectionLevel=None,setTagsToCount=["img"]
                                          ),
                        TagCountFeaturePerLengthFeature("Images per section","The ratio between the number of links (considering the  'img' HTML tag) and the section count","",
                                          FeatureVisibilityEnum.public, 
                                          FormatEnum.HTML, 
                                          FeatureTimePerDocumentEnum.MILLISECONDS,
                                          intCountLengthType=TagCountFeaturePerLengthFeature.SECTION_COUNT,intSectionLevel=None,setTagsToCount=["img"]
                                          ),                       
                       ]
        

        
        
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
        
        featSentenceCount = SentenceCountFeature("Phrase count","Number of phrases in the text.","",
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS)
        
        featLargeSentenceCount = LargeSentenceCountFeature("Large phrase Count","Count the number of phrases larger than a specified threshold.",
                                                           "reference",FeatureVisibilityEnum.public,FormatEnum.text_plain,
                                                           FeatureTimePerDocumentEnum.MICROSECONDS,10)
        
        featLargeSentenceCount.addConfigurableParam(ConfigurableParam("intSize","Sentence size",
                                                                      "The sentence need to have (at least) this length (in words) in order to be considered a large phrase.",
                                                                      10,ParamTypeEnum.int))
        
        featLargestSentenceSize = LargeSentenceSizeFeature("Largest phrase size","Compute the size of the largest phrase.",
                                                           "",FeatureVisibilityEnum.public,FormatEnum.text_plain,
                                                           FeatureTimePerDocumentEnum.MICROSECONDS,10)
        
        featLargePhraseRate = PhraseRateMoreThanAvgFeature("Large phrase rate","Percentage of phrases whose length is t words more than the average phrase length. Where t is the parameter 'Size threshold'.",
                                                           "",FeatureVisibilityEnum.public,FormatEnum.text_plain,
                                                           FeatureTimePerDocumentEnum.MICROSECONDS,10,bolLarge=True,intSize=10)
        featLargePhraseRate.addConfigurableParam(ConfigurableParam("intSize","Size threshold",
                                                                      "The phrase need to have (at least) this length more than the average in order to be considered a large sentence. The length is calculated using the number of words.",
                                                                      10,ParamTypeEnum.int))
        
        featShortPhraseRate = PhraseRateMoreThanAvgFeature("Short phrase rate","Percentage of phrases whose length is t words less than the average phrase length. Where t is the parameter 'Size threshold'.",
                                                           "",FeatureVisibilityEnum.public,FormatEnum.text_plain,
                                                           FeatureTimePerDocumentEnum.MICROSECONDS,10,bolLarge=True,intSize=5)
        featShortPhraseRate.addConfigurableParam(ConfigurableParam("intSize","Size threshold",
                                                                      "The phrase need to have (at most) this length less than the average in order to be considered a short sentence. The length is calculated using the number of words.",
                                                                      5,ParamTypeEnum.int))        
                
        featParagraphCount = ParagraphCountFeature("Paragraph Count","Count the number of paragraph at text",
                                         "reference",
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS)
        
        featLargeParagraphCount = LargeParagraphCountFeature("Large Paragraph Count","The number of paragraphs larger than a specified threshold",
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
    IS_LANGUAGE_DEPENDENT = True
    def __init__(self,objLanguage):
        super(FeatureFactory,self).__init__()
        self.objLanguage = objLanguage
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.BASE_DIR = os.path.abspath(os.path.join(self.BASE_DIR,os.pardir))
    
    
    def getClasseGramatical(self, str_classe):
        
        fileClasseGramatical = self.BASE_DIR+"/partOfSpeech/"+self.objLanguage.name+"/" + str_classe + ".txt"
        with open(fileClasseGramatical) as file:
            listPrepositions = file.read().split(",")
        
        return listPrepositions
    
    def createFeatureObject(self,classe):
        listWords = self.getClasseGramatical(classe)
        objFeature = WordCountFeature(str(classe).title() + " Count","Count the number of "+ classe +" in the text.",
                        "Based on file style.c from the file diction-1.11.tar.gz in http://ftp.gnu.org/gnu/diction/",
                        FeatureVisibilityEnum.public, 
                        FormatEnum.text_plain,FeatureTimePerDocumentEnum.MICROSECONDS,listWords,False)
        
        return objFeature
    
    def createBeginningOfSentenceFeatureObject(self,classe):
        listWords = self.getClasseGramatical(classe)
        n = ""
        if(classe[0] in set(["a","e","i","o","u"])):
            n = "n"
        objFeature = BeginningSentenceWordCountFeature("Sentences starting with a"+n+" "+str(classe).title(),"Count the number of phrases that starts with a"+n+" "+ classe +" in the text.",
                        "Based on file style.c from the file diction-1.11.tar.gz in http://ftp.gnu.org/gnu/diction/",
                        FeatureVisibilityEnum.public, 
                        FormatEnum.text_plain,FeatureTimePerDocumentEnum.MICROSECONDS,listWords,False)
        
        return objFeature
    
    def createFeatures(self):
        
        part_of_speech = ["articles","auxiliaryVerbs","coordinatingConjunctions","correlativeConjunctions",
                          "indefinitePronouns","interrogativePronouns","prepositions","pronouns",
                          "relativePronouns","subordinatingConjunctions","toBeVerbs"]
        
        
        arrFeatures = [self.createFeatureObject(classe) for classe in part_of_speech]
        [arrFeatures.append(self.createBeginningOfSentenceFeatureObject(classe)) for classe in part_of_speech]
        return arrFeatures
