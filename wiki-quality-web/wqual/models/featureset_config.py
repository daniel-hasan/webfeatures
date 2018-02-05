# -*- coding: utf-8 -*-
'''
Created on 13 de ago de 2017

@author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
Tabelas responsáveis por armazenar a configuração, definida pelo usuário, do conjunto de feature.
'''
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
import json
from feature.features import ParamTypeEnum, FeatureVisibilityEnum
from utils.basic_entities import LanguageEnum, FeatureTimePerDocumentEnum,\
    FormatEnum
from wqual.models.utils import Format
from wqual.models.utils import EnumManager, EnumModel
from utils.feature_utils import get_class_by_name
from decimal import Decimal

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
    

class FeatureFactory(models.Model):
    '''
    Created on 13 de ago de 2017

    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    FeatureFactory usados para obter as instancias de features.feature.FeatureCalculator a serem usados
    As classes inseridas devem ser subclasses de feature_factory.FeatureFactory
    '''
    nam_module = models.CharField( max_length=45)
    nam_factory_class = models.CharField( max_length=45) 
    
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
    nam_feature_set = models.CharField(max_length=50)
    dsc_feature_set = models.CharField(max_length=255, blank=True, null=True)
    
    language = models.ForeignKey(Language, models.PROTECT)  
    user = models.ForeignKey(User, models.PROTECT)
    
    
    def __str__(self):
        return "{name}: {description} ".format(name=self.nam_feature_set, description=self.dsc_feature_set)

    
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
    '''
    Created on 23 de dez de 2017

    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    Métodos que auxiliares para consultas/inserção/exclusão de feature sets
    '''
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

    
    feature_set = models.ForeignKey(FeatureSet, models.PROTECT)
    feature = models.ForeignKey(Feature, models.PROTECT)
    feature_time_to_extract = models.ForeignKey(FeatureTimePerDocument,models.PROTECT)
    feature_visibility = models.ForeignKey(FeatureVisibility,models.PROTECT)
    text_format = models.ForeignKey(Format,models.PROTECT)
    objects = UsedFeatureManager()
    
    def get_feature_instance(self):
        FeatureClass = self.feature.get_feature_class()
        param = {
            "visibility": self.feature_visibility.get_enum(),
            "text_format": self.text_format.get_enum(),
            "feature_time_per_document": self.feature_time_to_extract.get_enum()
        }        
        for arg in self.usedfeatureargval_set.all():
            if arg.type_argument == UsedFeatureArgVal.INT:
                param[arg.nam_argument] = int(arg.val_argument)
            elif arg.type_argument == UsedFeatureArgVal.JSON:
                param[arg.nam_argument] = json.loads(arg.val_argument)
            else:
                param[arg.nam_argument] = arg.val_argument

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
    STRING = "string"
    JSON = "json"
    TIPOS_DADOS = [(INT,"int"),(STRING,"string"),(JSON,"json")]

    nam_argument = models.CharField(max_length=45)
    val_argument = models.CharField(max_length=45)
    type_argument = models.CharField(max_length=10,choices=TIPOS_DADOS,default=STRING)
    
    is_configurable = models.BooleanField(default=False)
    used_feature = models.ForeignKey(UsedFeature, models.PROTECT)
     
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
    
