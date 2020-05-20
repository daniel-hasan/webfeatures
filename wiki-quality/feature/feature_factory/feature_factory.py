# -*- coding: utf-8 -*-
'''
Created on 8 de ago de  2017

@author: hasan
'''
from abc import abstractmethod
from feature.featureImpl.semantic_features import POSTaggerTrainerFeature, POSClassifierTrainerFeature
from feature.features import ConfigurableParam, ParamTypeEnum
from feature.featureImpl.readability_features import ARIFeature, \
    ColemanLiauFeature, FleschReadingEaseFeature, FleschKincaidFeature, \
    GunningFogIndexFeature, LasbarhetsindexFeature, \
    SmogGradingFeature
from feature.featureImpl.structure_features import *
from feature.featureImpl.style_features import *
from feature.featureImpl.semantic_features import *
from feature.featureImpl.graph import *
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

        arrFeatures = [TagCountFeature("Section count", "Count the number of sections (i.e. HTML h1 tags) in the text", "",
                                         FeatureVisibilityEnum.public,
                                         FormatEnum.HTML,
                                         FeatureTimePerDocumentEnum.MILLISECONDS,["h1"]),
                       TagCountFeature("Subsection count", "Count the number of subsections (i.e. HTML h1 tags) in the text", "",
                                         FeatureVisibilityEnum.public,
                                         FormatEnum.HTML,
                                         FeatureTimePerDocumentEnum.MILLISECONDS,["h2"]),
                       LinkCountFeature("Complete URL link count", "Count the number of  HTML 'a' tag in which the 'href' attribute refers to a complete URL.", "",
                                         FeatureVisibilityEnum.public,
                                         FormatEnum.HTML,
                                         FeatureTimePerDocumentEnum.MILLISECONDS,bolExternal=True,bolInternalSameDomain=False,bolInternalSamePage=False),
                       LinkCountFeature("Complete URL link count per section", "Ration between number of  HTML 'a' tag in which the 'href' attribute refers to a complete URL and the number of sections.", "",
                                         FeatureVisibilityEnum.public,
                                         FormatEnum.HTML,
                                         FeatureTimePerDocumentEnum.MILLISECONDS,
                                         bolExternal=True,bolInternalSameDomain=False,bolInternalSamePage=False,
                                         intPropotionalTo=Proportional.SECTION_COUNT.value
                                        ),
                       LinkCountFeature("Complete URL link count per length", "Ration between number of  HTML 'a' tag in which the 'href' attribute refers to a complete URL and the number of characters in text.", "",
                                         FeatureVisibilityEnum.public,
                                         FormatEnum.HTML,
                                         FeatureTimePerDocumentEnum.MILLISECONDS,
                                         bolExternal=True,bolInternalSameDomain=False,bolInternalSamePage=False,
                                         intPropotionalTo=Proportional.CHAR_COUNT.value
                                        ),
                       LinkCountFeature("Relative URL link count", "Count the number of  HTML 'a' tag in which the 'href' attribute refers to a relative URL (e.g. /images/cow.gif).", "",
                                         FeatureVisibilityEnum.public,
                                         FormatEnum.HTML,
                                         FeatureTimePerDocumentEnum.MILLISECONDS,
                                         bolExternal=False,bolInternalSameDomain=True,bolInternalSamePage=False),
                       LinkCountFeature("Relative URL link count per section", "Ratio between the number of  HTML 'a' tag in which the 'href' attribute refers to a relative URL (e.g. /images/cow.gif) and the number of sections.", "",
                                         FeatureVisibilityEnum.public,
                                         FormatEnum.HTML,
                                         FeatureTimePerDocumentEnum.MILLISECONDS,
                                         bolExternal=False,bolInternalSameDomain=True,bolInternalSamePage=False,
                                         intPropotionalTo=Proportional.SECTION_COUNT.value
                                         ),
                       LinkCountFeature("Relative URL link count per length", "Ratio between the number of  HTML 'a' tag in which the 'href' attribute refers to a relative URL (e.g. /images/cow.gif) and the number of characters in text.", "",
                                         FeatureVisibilityEnum.public,
                                         FormatEnum.HTML,
                                         FeatureTimePerDocumentEnum.MILLISECONDS,
                                         bolExternal=False,bolInternalSameDomain=True,bolInternalSamePage=False,
                                         intPropotionalTo=Proportional.CHAR_COUNT.value
                                         ),
                       LinkCountFeature("Same page link count", "Count the number of links which refers to some other elements in the same page."+
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
                       AverageSectionSize("Mean subsection size","The ratio between the section size (in characters) and the section count","",
                                          FeatureVisibilityEnum.public,
                                          FormatEnum.HTML,
                                          FeatureTimePerDocumentEnum.MILLISECONDS,2
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
                       TagCountFeature("Images count","Number of images (considering the 'img' HTML tag)","",
                                          FeatureVisibilityEnum.public,
                                          FormatEnum.HTML,
                                          FeatureTimePerDocumentEnum.MILLISECONDS,setTagsToCount=["img"]
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
                        TagCountFeature("Images per subsection","The ratio between the number of links (considering the  'img' HTML tag) and the subsection count","",
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

        featLargeSentenceCount = LargeSentenceCountFeature("Large phrase count","Count the number of phrases larger than a specified threshold.",
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

        featParagraphCount = ParagraphCountFeature("Paragraph count","Count the number of paragraph at text",
                                         "",
                                         FeatureVisibilityEnum.public,
                                         FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS)

        featLargeParagraphCount = LargeParagraphCountFeature("Large paragraph count","The number of paragraphs larger than a specified threshold",
                                         "",
                                         FeatureVisibilityEnum.public,
                                         FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS,16)

        featLargeParagraphCount.addConfigurableParam(ConfigurableParam("size","Paragraph size",
                                                                      "The paragraph need to have (at least) this length (in words) in order to be considered a large paragraph.",
                                                                      16,ParamTypeEnum.int))


        charCountFeat = CharacterCountFeature("Char Count","Count the number of characters in the text.","",
                    FeatureVisibilityEnum.public, FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS, ignore_punctuation=False)

        wordCountFeat = WordCountFeature("Word Count","Count the number of words in the text.","",
                    FeatureVisibilityEnum.public, FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS,ignore_punctuation=True)

        arrFeatures.append(featSentenceCount)
        arrFeatures.append(featLargeSentenceCount)
        arrFeatures.append(featParagraphCount)
        arrFeatures.append(featLargeParagraphCount)
        arrFeatures.append(featLargestSentenceSize)
        arrFeatures.append(featLargePhraseRate)
        arrFeatures.append(featShortPhraseRate)
        arrFeatures.append(charCountFeat)
        arrFeatures.append(wordCountFeat)

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
        strClassName = self.getWrittenName(classe)
        objFeature = WordCountFeature(strClassName[0].upper()+strClassName[1:]+ " count","Count the number of "+ strClassName +" in the text.",
                        "Based on 'style.c' file from the Software Style and Diction 1.11 in http://ftp.gnu.org/gnu/diction/",
                        FeatureVisibilityEnum.public,
                        FormatEnum.text_plain,FeatureTimePerDocumentEnum.MICROSECONDS,listWords,case_sensitive=False)

        return objFeature
    def getWrittenName(self,classe):
        dictClassName =  {"auxiliaryVerbs":"auxiliary verbs",
         "coordinatingConjunctions":"coordination conjunctions",
         "correlativeConjunctions":"correlative conjunctions",
         "indefinitePronouns":"indefinite pronouns",
         "interrogativePronouns": "interrogative pronouns",
         "relativePronouns":"relative pronoums",
        "subordinatingConjunctions":"subordinating conjunctions",
        "toBeVerbs":"to be verbs"}
        if(classe in dictClassName):
            return dictClassName[classe]
        return classe
    def createBeginningOfSentenceFeatureObject(self,classe):
        listWords = self.getClasseGramatical(classe)
        if(listWords == None):
            return None
        #n = ""
        #if(classe[0] in set(["a","e","i","o","u"])):
        #    n = "n"
        strClassName = self.getWrittenName(classe)
        objFeature = BeginningSentenceWordCountFeature("Sentences starting with "+strClassName,"Count the number of phrases that starts with "+ strClassName +" in the text. ",
                        "Based on 'style.c' file from the Software Style and Diction 1.11 in http://ftp.gnu.org/gnu/diction/",
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
        strReadabilityMetric = "Compute the {name} metric Based on 'style.c' file from the Software Style and Diction 1.11 in http://ftp.gnu.org/gnu/diction/."
        strRadabilityRefence = "Metric proposed by {author} in the article {article}."
        featARI = ARIFeature("ARI readability feature",
                strReadabilityMetric.format(name="Automated Readability Index"),
                  strRadabilityRefence.format(author="Smith E. A. and R. J. Senter",article="Automated readability index - Aerospace Medical Division (1967)"),
                  FeatureVisibilityEnum.public,
                  FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS)

        featColemanLiau = ColemanLiauFeature("Coleman-Liau readability feature",
                            strReadabilityMetric.format(name="Coleman-Liau metric"),
                            strRadabilityRefence.format(author="Meri Coleman and T. L. Liau",article="'A computer readability formula designed for machine scoring' - Journal of Applied Psychology (1975)"),
                            FeatureVisibilityEnum.public,
                            FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS)

        featFleschReadingEase = FleschReadingEaseFeature("Flesch Reading Ease Readability Feature",
                             strReadabilityMetric.format(name="Flesch Reading Ease"),
                             strRadabilityRefence.format(author="Flesch, R.",article="A New Readability Yardstick - Journal of Applied Psychology (1948)"),
                            FeatureVisibilityEnum.public,
                            FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS)

        featFleschKincaid = FleschKincaidFeature("Flesch Kincaid Readability Feature",
                strReadabilityMetric.format(name="Flesch Kincaid"),
                  strRadabilityRefence.format(author="Sandy Ressler",article="Perspectives on electronic publishing: standards, solutions, and more (1993)"),
                            FeatureVisibilityEnum.public,
                            FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS)

        featGunningFogIndex = GunningFogIndexFeature("Gunning Fog Index readability feature",
                strReadabilityMetric.format(name="Gunning Fog"),
                  strRadabilityRefence.format(author="R. Gunning",article="The Technique of Clear Writing (1952)"),
                            FeatureVisibilityEnum.public,
                            FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS)

        featLasbarhetsindex = LasbarhetsindexFeature("Lasbarhetsindex readability feature",
                 strReadabilityMetric.format(name="Lasbarhetsindex"),
                  strRadabilityRefence.format(author="C. Björnsson",article="Lesbarkeit durch Lix (1968)"),
                            FeatureVisibilityEnum.public,
                            FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS)

        featSmogGrading = SmogGradingFeature("SMOG Grading readability feature",
                            strReadabilityMetric.format(name="SMOG Grading"),
                            strRadabilityRefence.format(author="G. Harry McLaughlin",article="SMOG grading: A new readability formula (1969)"),
                            FeatureVisibilityEnum.public,
                            FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS)

        arrFeatures.append(featARI)
        arrFeatures.append(featColemanLiau)
        arrFeatures.append(featFleschReadingEase)
        arrFeatures.append(featFleschKincaid)
        arrFeatures.append(featGunningFogIndex)
        arrFeatures.append(featLasbarhetsindex)
        arrFeatures.append(featSmogGrading)

        return arrFeatures

class POSTaggerFeatureFactory(FeatureFactory):
    DEVELOPMENT = True
    IS_LANGUAGE_DEPENDENT = True
    def __init__(self,objLanguage):
        super(FeatureFactory,self).__init__()
        self.objLanguage = objLanguage
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.BASE_DIR = os.path.abspath(os.path.join(self.BASE_DIR,os.pardir))

    def createFeatures(self):

        arrFeatures = [ ]
        featPOSTaggerFeature = PartOfSpeechTaggerFeature("POS Tagger", "Part of speech tagger",
                                "Based on nltk's tagger library", FeatureVisibilityEnum.public,
                                FormatEnum.text_plain,FeatureTimePerDocumentEnum.MICROSECONDS,language=self.objLanguage.name)

        featBagOfPOS = BagOfPOSFeature("Bag of POS", "Bag of part of speech in text", "",
                        FeatureVisibilityEnum.public, FormatEnum.text_plain, FeatureTimePerDocumentEnum.MILLISECONDS,
                        language=self.objLanguage.name)

        arrFeatures.append(featPOSTaggerFeature)
        arrFeatures.append(featBagOfPOS)

        return arrFeatures

class GraphFeatureFactory(FeatureFactory):
    DEVELOPMENT = True
    def createFeatures(self):
                arrFeaturesImplementadas = [Indegree("Indegree","Indegree Metric metric","reference", FeatureVisibilityEnum.public,
                                                    FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS),
                                        Outdegree("Outdegree","Outdegree Metric of vertex","reference", FeatureVisibilityEnum.public,
                                                                            FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS),
                                        AssortativeInputInput("Assortative Input Input", "Assortative Input/Input Metric", "reference",
                                                    FeatureVisibilityEnum.public,FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS),
                                        AssortativeInputOutput("Assortative Input Output", "Assortative Input/Output Metric", "reference", FeatureVisibilityEnum.public,
                                                    FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS),
                                        AssortativeOutputInput("Assortative Output Input", "Assortative Output/Input Metric", "reference", FeatureVisibilityEnum.public,
                                                        FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS),
                                        AssortativeOutputOutput("Assortative Output Output", "Assortative Output/Output Metric", "reference", FeatureVisibilityEnum.public,
                                                        FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS),
                                        PageRank("PageRank", "PageRank Metric say how much popular is this article","reference", FeatureVisibilityEnum.public,
                                                FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS,0.95,0.01),
                                        ClusteringCoefficient("Clustering Coefficient","In graph theory, a clustering coefficient is a measure of the degree to which nodes in a graph tend to cluster together.","reference", FeatureVisibilityEnum.public,
                                                FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS,1)
                                                ]

                pr = PageRank("PageRank", "PageRank Metric say how much popular is this article","reference", FeatureVisibilityEnum.public,
                        FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS,0.85,0.01)
                pr.addConfigurableParam(ConfigurableParam("damping_factor","Damping Factor",
                                                                              "Damping Factor.",
                                                                              0.85,ParamTypeEnum.float))
                pr.addConfigurableParam(ConfigurableParam("convergence","Convergence",
                                                                            "Convergence.",
                                                                                0.01,ParamTypeEnum.float))

                #a parte do clustering não foi feita pelo Hasan.
                cc= ClusteringCoefficient("Clustering Coefficient","In graph theory, a clustering coefficient is a measure of the degree to which nodes in a graph tend to cluster together.","reference", FeatureVisibilityEnum.public,
                        FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS,1)
                cc.addConfigurableParam(ConfigurableParam("distance", "Distance",
                                                                            "Distance.",
                                                                                1.0, ParamTypeEnum.float))

                arrFeaturesImplementadas.append(pr)
                arrFeaturesImplementadas.append(cc)

                return arrFeaturesImplementadas
