# -*- coding: utf-8 -*-
'''
Created on 8 de ago de 2017

@author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
'''
from abc import abstractmethod
from enum import Enum

class Document(object):
    def __init__(self,int_doc_id,str_doc_name,str_text):
        self.int_doc_id = int_doc_id
        self.str_doc_name = str_doc_name
        self.str_text = str_text
        
class FeatureDocumentsWriter(object):
    @abstractmethod
    def write_document(self,document, arr_feats_used, arr_feats_result):
        raise NotImplementedError("Voce deve criar uma subclasse e a mesma deve sobrepor este método")
    
class FeatureDocumentsReader(object):
    '''
            Classe abstrata para a leitura dos textos 
            de um conjunto de documentos. Implemente este 
            leitor nos demais modulos para a leitura dos documentos.
            @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br> 
    '''
    @abstractmethod
    def get_documents(self):
        '''
            Método abstrato que retorna os documentos a serem lidos. 
            Este método
            deverá ser implementado nas subclasses.
            A clausula yield pode ser útil para implementar este método. Ver exemplo em DocSetReaderDummy.
            
            @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br> 
        '''
        raise NotImplementedError("Voce deve criar uma subclasse e a mesma deve sobrepor este método")
    
class DocSetReaderDummy(FeatureDocumentsReader):
    def get_documents(self):
        yield Document(1,"doc1","Ola meu nome é hasan")
        yield Document(2,"doc2","ipi ipi ura")
        yield Document(3,"doc3","lalala")
        
#class FeatureClassToExtract(object):
#    def __init__(self,feature_class,arr_feature_arguments):
#        self.feature_class = feature_class
#        self.arr_feature_arguments = arr_feature_arguments
    
#    def instantiate_feature(self):
#        module = __import__( "feature" )
#        Klass = getattr(module,self.feature_class)
#        return Klass(**self.arr_feature_arguments)
    
class FeatureCalculatorManager(object):

    def computeFeatureSetDocuments(self,datReader,docWriter,arr_features_to_extract,format):
        '''
            a partir de um diretorio FeatureDocumentsReader extrai as features de todos os textos.
            arr_features_to_extract são implementações da classe Feature calculator
            devem ser tranformados em um array de features para chamar, para cada documento,
            o método computeFeatureSet.
            @author: 
        '''
            #cria um array arr_features (array de FeatureCalculator)
            # com as features do array arr_features_to_extract

            # Rodar todos os docuemntos para todas as features que não
            # necessitam de algum metodo de preprocessamento de todo o conjunto de documento
        for doc in datReader.get_documents():
            pass
                
            #Para cada um processamento do documentSet necessário,
            # rodar todas as features que necessitam dele. 
            
            #
            
            
            
        pass
    
    
    
    def computeFeatureSet(self,docText,arr_features):
        '''
        Analisa o texto e calcula todas as features do array.
        Primeiro é calculada as features do formato HTML, depois, textplain. 
                 
        [fazer depois a parte de preprocessamento] Para cada formato:  Agrupa o conjunto de fetures no tipo 
        de preprocessamento do texto. Faz o preprocessamento roda as features para 
        este determinado preprocessamento. 
        
        Rode primeiramente todas as TextBasedFeature usando
        o texto completo e, logo apos, para cada palavra, rode todas as WordCountFeatures
        
           
        Saída: arranjo para cada posicao de arrFeature, a resposta da feture correspondente
        
        @author:  
        '''
        pass
class FeatureVisibilityEnum(Enum):
    '''
        Enum responsável pela visibilidade das features
        @author:  Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    '''
    public = "Visibilidade total"
    local = "Visibilidade nas interfaces (web e de caracteres, por ex) apenas se for localhost"
    private = "Não serão visualizadas nas interfaces (web e de caracteres) apenas rodando na linha de comando"    
    
class FeatureCalculator(object):
    '''
        Classe abstrata das features. Os demais módulos deverão acessar as 
        features apenas por meio desta classe. 
        @author:  Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    '''
    featureManager = FeatureCalculatorManager()
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        
        self.name = name
        self.description = description
        self.reference = reference
        self.visibility = visibility
        self.text_format = text_format
        self.feature_time_per_document = feature_time_per_document
        self.arr_configurable_param = []
        
    def addConfigurableParam(self,objParam):
        self.arr_configurable_param.append(objParam)
    
    
     
class TextBasedFeature(FeatureCalculator):
    '''
    São subclasses desta classe abstrata as features que NÃO conseguem 
    analisar o texto por palavra para efetuar o calculo desta feature.
    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    '''
    @abstractmethod
    def compute_feature(self,document):
        raise NotImplementedError


class WordBasedFeature(FeatureCalculator):
    '''
    São subclasses desta classe abstrata as features que conseguem 
    analisar o texto por palavra para efetuar o calculo desta feature.
    
    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    '''
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):
        super(FeatureCalculator,self).__init__(name,description,reference,visibility,text_format,feature_time_per_document)   
    
    @abstractmethod
    def checkWord(self,document,word):
        raise NotImplementedError
    
    
    @abstractmethod
    def feature_result(self,document):
        raise NotImplementedError




            
    
class ParamTypeEnum(Enum):
    '''
        Tipo do valor de um parametro de uma feature.
        @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>    
    '''
    int = "int"
    float = "float"
    string = "string"
    choices = "choices"
    
class ConfigurableParam(object):
    '''
        Classe que armazena os parametros de uma feature que são configuráveis pelo usuário.
        @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>    
    '''
    def __init__(self,att_name,name,description,default_value,param_type,arr_choices=[]):
        self.name = name
        self.att_name = att_name
        self.description = description
        self.default_value = default_value
        self.param_type = param_type
        self.arr_choices = arr_choices