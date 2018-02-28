# -*- coding: utf-8 -*-
'''
Created on 8 de ago de 2017

@author: hasan
'''
from abc import abstractmethod
from django.contrib.sessions.backends import file

from feature import ConfigurableParam, ParamTypeEnum
from feature.featureImpl.readability_features import ARIFeature, \
    ColemanLiauFeature, FleschReadingEaseFeature, FleschKincaidFeature, \
    GunningFogIndexFeature, LasbarhetsindexFeature, \
    SmogGradingFeature
from feature.featureImpl.structure_features import *
from feature.featureImpl.style_features import *
from feature.features import  FeatureVisibilityEnum
from utils.basic_entities import FormatEnum, FeatureTimePerDocumentEnum

 
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
                                         FeatureTimePerDocumentEnum.MILLISECONDS,bolExternal=True,bolInternalSameDomain=False,bolInternalSamePage=False),
                       LinkCountFeature("Complete URL link Count per section", "Ration between number of  HTML 'a' tag in which the 'href' attribute refers to a complete URL and the number of sections.", "", 
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.HTML, 
                                         FeatureTimePerDocumentEnum.MILLISECONDS,
                                         bolExternal=True,bolInternalSameDomain=False,bolInternalSamePage=False,
                                         intPropotionalTo=Proportional.SECTION_COUNT.value
                                        ),
                       LinkCountFeature("Complete URL link Count per length", "Ration between number of  HTML 'a' tag in which the 'href' attribute refers to a complete URL and the number of characters in text.", "", 
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.HTML, 
                                         FeatureTimePerDocumentEnum.MILLISECONDS,
                                         bolExternal=True,bolInternalSameDomain=False,bolInternalSamePage=False,
                                         intPropotionalTo=Proportional.CHAR_COUNT.value
                                        ),                       
                       LinkCountFeature("Relative URL link Count", "Count the number of  HTML 'a' tag in which the 'href' attribute refers to a relative URL (e.g. /images/cow.gif).", "", 
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.HTML, 
                                         FeatureTimePerDocumentEnum.MILLISECONDS,
                                         bolExternal=False,bolInternalSameDomain=True,bolInternalSamePage=False),
                       LinkCountFeature("Relative URL link Count per section", "Ratio between the number of  HTML 'a' tag in which the 'href' attribute refers to a relative URL (e.g. /images/cow.gif) and the number of sections.", "", 
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.HTML, 
                                         FeatureTimePerDocumentEnum.MILLISECONDS,
                                         bolExternal=False,bolInternalSameDomain=True,bolInternalSamePage=False,
                                         intPropotionalTo=Proportional.SECTION_COUNT.value
                                         ),     
                       LinkCountFeature("Relative URL link Count per length", "Ratio between the number of  HTML 'a' tag in which the 'href' attribute refers to a relative URL (e.g. /images/cow.gif) and the number of characters in text.", "", 
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.HTML, 
                                         FeatureTimePerDocumentEnum.MILLISECONDS,
                                         bolExternal=False,bolInternalSameDomain=True,bolInternalSamePage=False,
                                         intPropotionalTo=Proportional.CHAR_COUNT.value
                                         ),                                           
                       LinkCountFeature("Same page link Count", "Count the number of links which refers to some other elements in the same page."+
                                                                " In other words, count the number of HTML 'a' tags in which 'href' points to some html page id."+
                                                                " For example, the value '#mainDiv' point to an element in the page which the id is 'mainDiv'.", "", 
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.HTML, 
                                         FeatureTimePerDocumentEnum.MILLISECONDS,
                                         bolExternal=False,bolInternalSameDomain=False,bolInternalSamePage=True),

                       LinkCountFeature("Same page link count per section", "The ratio between the number of links which refers to some other elements in the same page and the number of sections", "", 
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.HTML, 
                                         FeatureTimePerDocumentEnum.MILLISECONDS,
                                         bolExternal=False,bolInternalSameDomain=False,bolInternalSamePage=True,
                                         intPropotionalTo=Proportional.SECTION_COUNT.value),
                        LinkCountFeature("Same page link count per length", "The ratio between the number of links which refers to some other elements in the same page and the number of characters in text.", "", 
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.HTML, 
                                         FeatureTimePerDocumentEnum.MILLISECONDS,
                                         bolExternal=False,bolInternalSameDomain=False,bolInternalSamePage=True,
                                         intPropotionalTo=Proportional.CHAR_COUNT.value),                      
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
                       
                        TagCountFeature("Images per length","Number of images (considering the 'img' HTML tag) per length (in characters)","",
                                          FeatureVisibilityEnum.public, 
                                          FormatEnum.HTML, 
                                          FeatureTimePerDocumentEnum.MILLISECONDS,
                                          intPropotionalTo=Proportional.CHAR_COUNT.value,setTagsToCount=["img"]
                                          ),
                        TagCountFeature("Images per section","The ratio between the number of links (considering the  'img' HTML tag) and the section count","",
                                          FeatureVisibilityEnum.public, 
                                          FormatEnum.HTML, 
                                          FeatureTimePerDocumentEnum.MILLISECONDS,
                                          intPropotionalTo=Proportional.SECTION_COUNT.value,setTagsToCount=["img"]
                                          ),                       
                       ]
        

        
        
        #featTagCount = TagCountFeature("Section div Count", "Count the number of HTML div sections in the text", "reference", 
        #                                 FeatureVisibilityEnum.public, 
        #                                 FormatEnum.HTML, 
        #                                 FeatureTimePerDocumentEnum.MILLISECONDS,["div"])
        #arrFeatures.append(featTagCount)
        return arrFeatures
class StyleFeatureFactory(FeatureFactory):
    def createFeatures(self):
        '''
        Cria as features de estilo de escrita (numero de preposicoes, pronomes, etc).
        Parametros:
        '''
        
        arrFeatures = []
        
        featSentenceCount = SentenceCountFeature("Phrase count","Number of phrases in the text.","",
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS)
        
        featLargeSentenceCount = LargeSentenceCountFeature("Large Phrase Count","Count the number of phrases larger than a specified threshold.",
                                                           "reference",FeatureVisibilityEnum.public,FormatEnum.text_plain,
                                                           FeatureTimePerDocumentEnum.MICROSECONDS,10)
        
        featLargeSentenceCount.addConfigurableParam(ConfigurableParam("int_size","Sentence Size",
                                                                      "The sentence need to have (at least) this length (in words) in order to be considered a large phrase.",
                                                                      10,ParamTypeEnum.int))
        
        featLargestSentenceSize = LargeSentenceSizeFeature("Largest phrase size","Compute the size of the largest phrase.",
                                                               "",FeatureVisibilityEnum.public,FormatEnum.text_plain,
                                                               FeatureTimePerDocumentEnum.MICROSECONDS)
            
        featLargePhraseRate = PhraseRateMoreThanAvgFeature("Large phrase rate","Percentage of phrases whose length is t words more than the average phrase length. Where t is the parameter 'Size threshold'.",
                                                               "",FeatureVisibilityEnum.public,FormatEnum.text_plain,
                                                               FeatureTimePerDocumentEnum.MICROSECONDS,bolLarge=True,intSize=2)
            
        featShortPhraseRate = PhraseRateMoreThanAvgFeature("Short phrase rate","Percentage of phrases whose length is t words less than the average phrase length. Where t is the parameter 'Size threshold'.",
                                                               "",FeatureVisibilityEnum.public,FormatEnum.text_plain,
                                                               FeatureTimePerDocumentEnum.MICROSECONDS,bolLarge=False,intSize=2)                
        featLargePhraseRate.addConfigurableParam(ConfigurableParam("intSize","Size threshold",
                                                                      "The phrase need to have (at least) this length more than the average in order to be considered a large sentence. The length is calculated using the number of words.",
                                                                      2,ParamTypeEnum.int))
        
        featShortPhraseRate.addConfigurableParam(ConfigurableParam("intSize","Size threshold",
                                                                      "The phrase need to have (at most) this length less than the average in order to be considered a short sentence. The length is calculated using the number of words.",
                                                                      2,ParamTypeEnum.int))        
                
        featParagraphCount = ParagraphCountFeature("Paragraph Count","Count the number of paragraph at text",
                                         "",
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS)
        
        featLargeParagraphCount = LargeParagraphCountFeature("Large Paragraph Count","The number of paragraphs larger than a specified threshold",
                                         "",
                                         FeatureVisibilityEnum.public, 
                                         FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS,16)
        
        featLargeParagraphCount.addConfigurableParam(ConfigurableParam("size","Paragraph Size",
                                                                      "The paragraph need to have (at least) this length (in words) in order to be considered a large paragraph.",
                                                                      16,ParamTypeEnum.int))
        
        
        
        arrFeatures.append(featSentenceCount)
        arrFeatures.append(featLargeSentenceCount)
        arrFeatures.append(featParagraphCount)
        arrFeatures.append(featLargeParagraphCount)
        arrFeatures.append(featLargestSentenceSize)
        arrFeatures.append(featLargePhraseRate)
        arrFeatures.append(featShortPhraseRate)
        return  arrFeatures
        

class WordsFeatureFactory(FeatureFactory):
    IS_LANGUAGE_DEPENDENT = True
    def __init__(self,objLanguage):
        super(FeatureFactory,self).__init__()
        self.objLanguage = objLanguage
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.BASE_DIR = os.path.abspath(os.path.join(self.BASE_DIR,os.pardir))
    
    
    def getClasseGramatical(self, str_classe):
        try: 
            fileClasseGramatical = self.BASE_DIR+"/partOfSpeech/"+self.objLanguage.name+"/" + str_classe + ".txt"
            with open(fileClasseGramatical) as file:
                listPrepositions = file.read().split(",")
        except FileNotFoundError:
            return None
        return listPrepositions
    
    def createFeatureObject(self,classe):
        listWords = self.getClasseGramatical(classe)
        if(listWords == None):
            return None
        objFeature = WordCountFeature(str(classe).title() + " Count","Count the number of "+ classe +" in the text.",
                        "Based on file style.c from the file diction-1.11.tar.gz in http://ftp.gnu.org/gnu/diction/",
                        FeatureVisibilityEnum.public, 
                        FormatEnum.text_plain,FeatureTimePerDocumentEnum.MICROSECONDS,listWords,case_sensitive=False)
        
        return objFeature
    
    def createBeginningOfSentenceFeatureObject(self,classe):
        listWords = self.getClasseGramatical(classe)
        if(listWords == None):
            return None
        n = ""
        if(classe[0] in set(["a","e","i","o","u"])):
            n = "n"
        objFeature = BeginningSentenceWordCountFeature("Sentences starting with a"+n+" "+str(classe).title(),"Count the number of phrases that starts with a"+n+" "+ classe +" in the text. ",
                        "Based on file style.c from the file diction-1.11.tar.gz in http://ftp.gnu.org/gnu/diction/",
                        FeatureVisibilityEnum.public, 
                        FormatEnum.text_plain,FeatureTimePerDocumentEnum.MICROSECONDS,listWords,False)
        
        return objFeature
    
    def createFeatures(self):
        
        part_of_speech = ["articles","auxiliaryVerbs","coordinatingConjunctions","correlativeConjunctions",
                          "indefinitePronouns","interrogativePronouns","prepositions","pronouns",
                          "relativePronouns","subordinatingConjunctions","toBeVerbs"]
        
        arrFeatures = [ ]
        for classe in part_of_speech:
            objFeature = self.createFeatureObject(classe)
            if(objFeature!=None):
                arrFeatures.append(objFeature)
                
        for classe in part_of_speech:
            objFeature = self.createBeginningOfSentenceFeatureObject(classe)
            if(objFeature != None):
                arrFeatures.append(objFeature)
        return arrFeatures


class ReadabilityFeatureFactory(FeatureFactory):
    
    def createFeatures(self):
        
        arrFeatures = []
        
        featARI = ARIFeature("ARI Readability Feature","Compute ARI metric",
                  "Based on Daniel Hasan Dalip's PhD thesis", FeatureVisibilityEnum.public,
                  FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS)
        
        featColemanLiau = ColemanLiauFeature("Coleman-Liau Readability Feature","Compute Coleman-Liau metric",
                            "Based on file style from the file diction-1.11.tar.gz in http://ftp.gnu.org/gnu/diction/"
                             + " and based on Coleman, et al. article 'A computer readability formula designed for machine scoring' - Journal of Applied Psychology (1975)",FeatureVisibilityEnum.public,
                            FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS)
        
        featFleschReadingEase = FleschReadingEaseFeature("Flesch Reading Ease Readability Feature","Compute Flesch Reading Ease metric",
                            "Based on Daniel Hasan Dalip's PhD thesis", FeatureVisibilityEnum.public,
                            FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS)
                
        featFleschKincaid = FleschKincaidFeature("Flesch Kincaid Readability Feature","Compute Flesch Kincaid metric",
                            "Based on Daniel Hasan Dalip's PhD thesis", FeatureVisibilityEnum.public,
                            FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS)
        
        featGunningFogIndex = GunningFogIndexFeature("Gunning Fog Index Readability Feature","Compute Gunning Fog Index metric",
                            "Based on Daniel Hasan Dalip's PhD thesis", FeatureVisibilityEnum.public,
                            FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS)
        
        featLasbarhetsindex = LasbarhetsindexFeature("Lasbarhetsindex Readability Feature","Compute Lasbarhetsindex metric",
                            "Based on Daniel Hasan Dalip's PhD thesis", FeatureVisibilityEnum.public,
                            FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS)
        
        featSmogGrading = SmogGradingFeature("Smog Grading Readability Feature","Compute Smog Grading metric",
                            "Based on Daniel Hasan Dalip's PhD thesis", FeatureVisibilityEnum.public,
                            FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS)
        
        arrFeatures.append(featARI)
        arrFeatures.append(featColemanLiau)
        arrFeatures.append(featFleschReadingEase)
        arrFeatures.append(featFleschKincaid)
        arrFeatures.append(featGunningFogIndex)
        arrFeatures.append(featLasbarhetsindex)
        arrFeatures.append(featSmogGrading)
        
        return arrFeatures