# -*- coding: utf-8 -*-
'''
Created on 13 de ago de 2017

@author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
Tabelas responsáveis por armazenar a configuração, definida pelo usuário, do conjunto de feature.
'''
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.template.defaultfilters import default
from django.db import models, transaction
import json
import inspect
from django_mysql.models import JSONField
from feature.features import ParamTypeEnum, FeatureVisibilityEnum
from utils.basic_entities import LanguageEnum, FeatureTimePerDocumentEnum,\
    FormatEnum
from wqual.models.utils import Format
from wqual.models.utils import EnumManager, EnumModel
from utils.feature_utils import get_class_by_name
from decimal import Decimal
from wqual.models.utils import EnumManager, EnumModel
from wqual.models.utils import Format


class Source(models.Model):
    '''
    Created on 2 de out de 2018

    @author: Gabriel Silva Brandão <gabriel.silva.brandao7@gmail.com>
    Indica o tipo de fonte de um FeatureSet, sendo que inicialmente temos os
    tipos Textual e grafo.
    '''
    id = models.IntegerField(primary_key=True, unique=True)
    nam_source = models.CharField( max_length=45)
    DEFAULT_SOURCE_ID=1
    SOURCES = [{"id":1,"nam_source":"Textual"},
                {"id":2,"nam_source":"Graph"},
                {"id":3,"nam_source":"Revision"}]
    def __str__(self):
        return self.nam_source

class Feature(models.Model):
    '''
    Created on 13 de ago de 2017

    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    Classe e módulo de uma feature usada. A classe deve ser subclasse de features.feature.FeatureCalculator.
    Essas classes são criadas a medida que vão sendo usadas. As classes/objetos das features usadas são obtidos pela classe
    FeatureFactory
    '''
    nam_module = models.CharField( max_length=45)
    nam_feature_class = models.CharField(max_length=255)

    def get_feature_class(self):
        return get_class_by_name(self.nam_module+"."+self.nam_feature_class)

class ParamType(EnumModel):
    '''
    Created on 13 de ago de 2017

    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    Tipo do parâmetro a ser usado ao instanciar uma feature
    '''
    @staticmethod
    def get_enum_class():
        return ParamTypeEnum

class FeatureFactoryManager(models.Manager):
    '''
    Created on 07 de fev de 2018

    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    '''
    def get_all_features_from_language(self,obj_language):
        arr_features = []
        for featFactory in self.all():

            #instantiate feature factory class
            FeatureFactoryClass = get_class_by_name(featFactory.nam_module+"."+featFactory.nam_factory_class)

            objFeatureFactory = None
            if FeatureFactoryClass.IS_LANGUAGE_DEPENDENT:
                objFeatureFactory = FeatureFactoryClass(obj_language.get_enum())
            else:
                objFeatureFactory = FeatureFactoryClass()

            #add all the features from factory
            arrNames = [f.name for f in objFeatureFactory.createFeatures()]
            #print("Feature: "+featFactory.nam_factory_class+" array: "+str(arrNames))
            [arr_features.append(objFeature) for objFeature in objFeatureFactory.createFeatures()]
        return arr_features


class FeatureFactory(models.Model):
    '''
    Created on 13 de ago de 2017

    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    FeatureFactory usados para obter as instancias de features.feature.FeatureCalculator a serem usados
    As classes inseridas devem ser subclasses de feature_factory.FeatureFactory
    '''

    nam_module = models.CharField( max_length=45)
    nam_factory_class = models.CharField( max_length=45)
    objects = FeatureFactoryManager()
    source = models.ForeignKey("Source", default=Source.DEFAULT_SOURCE_ID, on_delete=models.PROTECT)

    def get_class(self):
        '''
        resgata a classe com um vocabulario dependente de linguagem a ser usa
        @todo: Nem todos as linguas sao implementadas, deve-se lançar uma exceção e
        assim não criar a feature caso nao encontre a classe
        '''
        module = __import__( self.nam_module)
        Klass = getattr(module,self.nam_factory_class)
        return Klass

    class Meta:
        db_table = 'wqual_feature_factory'



class Language(EnumModel):
    '''
    Created on 13 de ago de 2017

    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    Lingua e código da lingua a ser usado para determinar, no conjunto de features (FeatureSet),
    a lingua que os atributos devem ser compatíveis. Deve haver a lingua "Multilingue".
    '''
    @staticmethod
    def get_enum_class():
        return LanguageEnum


    def __str__(self):
        return "[{code}] {language}".format(code=self.name,language=self.value)


class FeatureSet(models.Model):
    '''
    Created on 13 de ago de 2017

    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    Conjunto de features configurado por um usuário
    '''

    nam_feature_set = models.CharField(verbose_name="Feature set name",max_length=20)
    dsc_feature_set = models.CharField(verbose_name="Description",max_length=255, blank=True, null=True)
    bol_is_public = models.BooleanField(verbose_name="",default=False)

    language = models.ForeignKey(Language, models.PROTECT)
    user = models.ForeignKey(User, models.PROTECT)
    source = models.ForeignKey("Source", default=Source.DEFAULT_SOURCE_ID, on_delete=models.PROTECT)


    def __str__(self):
        #return "{name} : {description} : {id} ".format(name=self.nam_feature_set, description=self.dsc_feature_set, id=self.id)
        return self.nam_feature_set


    class Meta:
        db_table = 'wqual_feature_set'
        unique_together = (('nam_feature_set', 'user'),)
        indexes = [
            models.Index(fields=['nam_feature_set', 'user']),
        ]

from django.core.validators import MaxValueValidator

class FeatureTimePerDocument(EnumModel):
    '''
    Created on 17 de ago de 2017

    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>

    '''
    '''
    val_cost_time = models.DecimalField(max_digits=20,decimal_places=9) #,decimal_places=9, default=Decimal('0.0000'))

    def save(self, *args, **kwargs):
        if(self.name==FeatureTimePerDocumentEnum.MICROSECONDS):
            self.val_cost_time = 1/(10^6)
        elif(self.name==FeatureTimePerDocumentEnum.MILLISECONDS):
            self.val_cost_time = 1/(10^3)
        elif(self.name==FeatureTimePerDocumentEnum.SECONDS):
            self.val_cost_time = 1
        elif(self.name==FeatureTimePerDocumentEnum.MINUTES):
            self.val_cost_time = 60
        elif(self.name==FeatureTimePerDocumentEnum.HOURS):
            self.val_cost_time = 3600
        super().save(*args, **kwargs)
    '''

    @staticmethod
    def get_enum_class():
        return FeatureTimePerDocumentEnum

class FeatureVisibility(EnumModel):
    '''
    Created on 17 de ago de 2017

    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    '''
    @staticmethod
    def get_enum_class():
        return FeatureVisibilityEnum


class UsedFeatureManager(models.Manager):
    def from_obj_to_bd_type_val(self,value):
        paramType = None
        paramValue = value
        if(type(value)==str):
            paramType = UsedFeatureArgVal.STRING
        elif(type(value)==int):
            paramType = UsedFeatureArgVal.INT
        elif(type(value)==float):
            paramType = UsedFeatureArgVal.FLOAT
        elif(value == None):
            paramType = UsedFeatureArgVal.NONE_T
        elif(type(value)==bool):
            paramType = UsedFeatureArgVal.BOOLEAN
        elif type(value)==list or type(value)==dict:
            paramType = UsedFeatureArgVal.JSON
            paramValue = json.dumps(value)
        elif(type(value)==set):
            paramType = UsedFeatureArgVal.JSON_SET
            paramValue = [element for element in value]
            paramValue = json.dumps(paramValue)

        return paramType,paramValue
    def insert_features_object(self,featureSet,arrObjectFeatures):
        dictInsertedFeatPerName = {}
        with transaction.atomic():
            int_ord_feature = UsedFeature.objects.filter(feature_set=featureSet).count()+1
            for objFeature in arrObjectFeatures:
                #print("Inserindo Feature: "+objFeature.__class__.__name__)
                featureObj = Feature.objects.get_or_create(nam_module=objFeature.__module__, nam_feature_class=objFeature.__class__.__name__)[0]

                objFeatUsed = self.create(feature_set=featureSet,
                                            feature = featureObj,
                                            feature_time_to_extract=FeatureTimePerDocument.objects.get_enum(objFeature.feature_time_per_document),
                                            feature_visibility=FeatureVisibility.objects.get_enum(objFeature.visibility),
                                            text_format=Format.objects.get_enum(objFeature.text_format),
                                            ord_feature=int_ord_feature
                                            )
                dictInsertedFeatPerName[objFeature.name] = objFeatUsed
                #obtem todos os atributos do construtor (exceto o primeiro - self)
                arrParamsConstrutor = set(inspect.getargspec(objFeature.__init__).args[1:])
                dictParamsToInsert = {}
                #agrupa os parametros num dicionario (pelo nome do atributo)
                for name,value in objFeature.__dict__.items():
                    if(name in arrParamsConstrutor):
                        if name not in ("visibility","text_format","feature_time_per_document"):
                            paramType,paramValue = self.from_obj_to_bd_type_val(value)
                            dictParamsToInsert[name]= {"nam_att_argument":name,
                                                       "val_argument": str(paramValue),
                                                       "type_argument":paramType,
                                                       "is_configurable": False}

                #atualiza como configuraveis os parametros que estao como configuraveis
                for objConfigurableFeature in objFeature.arr_configurable_param:
                    if(objConfigurableFeature.att_name in dictParamsToInsert):
                        dictArgValToInsert = dictParamsToInsert[objConfigurableFeature.att_name]
                        if objConfigurableFeature.param_type == ParamTypeEnum.choices:
                            pass
                            #TODO: se for choices, armazenas as alternativas (arr_choices) no campo apropriado
                        dictArgValToInsert["nam_argument"] = objConfigurableFeature.name
                        dictArgValToInsert["val_argument"] = objConfigurableFeature.default_value
                        dictArgValToInsert["dsc_argument"] = objConfigurableFeature.description
                        dictArgValToInsert["is_configurable"] = True

                for dictArgValToInsert in dictParamsToInsert.values():
                    UsedFeatureArgVal.objects.create(    nam_argument = dictArgValToInsert["nam_argument"] if "nam_argument" in dictArgValToInsert else "",
                                                         nam_att_argument= dictArgValToInsert["nam_att_argument"],
                                                                 val_argument = dictArgValToInsert["val_argument"],
                                                                 dsc_argument = dictArgValToInsert["dsc_argument"] if "dsc_argument" in dictArgValToInsert else "",
                                                                 type_argument=dictArgValToInsert["type_argument"],
                                                                 is_configurable = dictArgValToInsert["is_configurable"],
                                                                 used_feature=objFeatUsed,
                                                                 )


                int_ord_feature = int_ord_feature+1
        return dictInsertedFeatPerName
    def get_html_features_name_grouped_by_featureset(self):
        arrUsedFeatures = UsedFeature.objects.prefetch_related("usedfeatureargval_set").filter(text_format__name=FormatEnum.HTML.name)
        mapFeaturesGroup = {}
        #navega em todos os used features
        #agrupando o nome das features
        for objUsed in list(arrUsedFeatures):
            mapFeaturesGroup[objUsed.feature_set_id] = []
            for arg in objUsed.usedfeatureargval_set.all():
                if(arg.nam_argument == "name"):
                    mapFeaturesGroup[objUsed.feature_set_id].append(arg.val_argument)
        return mapFeaturesGroup



class UsedFeature(models.Model):
    '''
    Created on 13 de ago de 2017

    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    Relação das features usadas por um usuário
    '''
    ord_feature = models.IntegerField()

    feature_set = models.ForeignKey(FeatureSet, models.CASCADE)
    feature = models.ForeignKey(Feature, models.PROTECT)
    feature_time_to_extract = models.ForeignKey(FeatureTimePerDocument,models.PROTECT)
    feature_visibility = models.ForeignKey(FeatureVisibility,models.PROTECT)
    text_format = models.ForeignKey(Format,models.PROTECT)
    objects = UsedFeatureManager()

    def get_features_with_params(self):

        arrConfigParamsFeat = []
        isConfigurable = False
        objFeature = self.get_feature_instance()
        for argValParam in self.usedfeatureargval_set.values("id","dsc_argument","nam_argument","val_argument","type_argument","is_configurable"):
            if(argValParam['is_configurable']):
                arrConfigParamsFeat.append(argValParam)
                isConfigurable = True

        #print("Parametros do "+objFeature.name+":"+str(arrConfigParamsFeat))
        return {"used_feature_id":self.id,
                 "name":objFeature.name,
                 "description":objFeature.description,
                 "reference":objFeature.reference,
                 "is_configurable":isConfigurable,
                 "ord_feature":self.ord_feature,
                 "arr_param":arrConfigParamsFeat,
                 "str_arr_param":objFeature.get_params_str()
                  }

    def get_feature_instance(self):
        FeatureClass = self.feature.get_feature_class()
        param = {
            "visibility": self.feature_visibility.get_enum(),
            "text_format": self.text_format.get_enum(),
            "feature_time_per_document": self.feature_time_to_extract.get_enum()
        }
        for arg in self.usedfeatureargval_set.all():
            if arg.type_argument == UsedFeatureArgVal.INT:
                param[arg.nam_att_argument] = int(arg.val_argument)
                #print("nome " + arg.nam_argument + "Valor " + arg.val_argument)
            elif arg.type_argument == UsedFeatureArgVal.FLOAT:
                param[arg.nam_att_argument] = float(arg.val_argument)
            elif arg.type_argument == UsedFeatureArgVal.NONE_T:
                param[arg.nam_att_argument] = None
            elif arg.type_argument == UsedFeatureArgVal.BOOLEAN:
                param[arg.nam_att_argument] = arg.val_argument.lower()=="true"
            elif arg.type_argument == UsedFeatureArgVal.JSON:
                param[arg.nam_att_argument] = json.loads(arg.val_argument)
            elif arg.type_argument == UsedFeatureArgVal.JSON_SET:
                param[arg.nam_att_argument] = set(json.loads(arg.val_argument))
            else:
                param[arg.nam_att_argument] = arg.val_argument

        obj = FeatureClass(**param)
        return obj
    class Meta:
        db_table = 'wqual_used_feature'

class UsedFeatureArgVal(models.Model):
    '''
    Created on 13 de ago de 2017

    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    Argumentos (i.e. parametros) usados para instanciar esta feature
    '''
    INT = "int"
    FLOAT = "float"
    STRING = "string"
    BOOLEAN = "boolean"
    NONE_T = "None"
    JSON = "json"
    JSON_SET = "json_set"
    TIPOS_DADOS = [(INT,"int"),(FLOAT,"float"),(STRING,"string"),(BOOLEAN,"boolean"),(JSON,"json"),(JSON_SET,"json_set")]

    nam_argument = models.CharField(max_length=45,blank=True, null=True)
    nam_att_argument = models.CharField(max_length=60)
    val_argument = models.CharField(max_length=5000)
    dsc_argument = models.CharField(max_length=255, blank=True, null=True)
    json_choices = JSONField(blank=True, null=True)

    type_argument = models.CharField(max_length=10,choices=TIPOS_DADOS,default=STRING)

    is_configurable = models.BooleanField(default=False)
    used_feature = models.ForeignKey(UsedFeature, models.CASCADE)

class FeatureConfigurableParam(models.Model):
    '''
    Created on 13 de ago de 2017

    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    Argumento usado para instanciar uma feature
    '''
    nam_feature = models.CharField(max_length=45)
    dsc_feature = models.CharField(max_length=255)
    dsc_arr_choices = models.CharField(max_length=255)

    param_type = models.ForeignKey(ParamType, models.PROTECT,blank=True, null=True)
    used_feature = models.OneToOneField(UsedFeatureArgVal, models.PROTECT)

    class Meta:
        db_table = 'wqual_feature_configurable_param'
