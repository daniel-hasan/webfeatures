# -*- coding: utf-8 -*-
'''
Created on 13 de ago de 2017

@author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
Tabelas responsáveis por armazenar a configuração, definida pelo usuário, do conjunto de feature.
'''
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from feature.features import ParamTypeEnum, FeatureVisibilityEnum
from utils.basic_entities import LanguageEnum, FeatureTimePerDocumentEnum
from wqual.models.utils import EnumManager, EnumModel


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
        
class FeatureTimePerDocument(EnumModel):
    '''
    Created on 17 de ago de 2017

    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
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
    
class UsedFeature(models.Model):
    '''
    Created on 13 de ago de 2017

    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    Relação das features usadas por um usuário
    '''
    feature_set = models.ForeignKey(FeatureSet, models.PROTECT)
    feature = models.ForeignKey(Feature, models.PROTECT)
    feature_time_to_extract = models.ForeignKey(FeatureTimePerDocument,models.PROTECT)
    feature_visibility = models.ForeignKey(FeatureVisibility,models.PROTECT)
    
    
    class Meta:
        db_table = 'wqual_used_feature'

class UsedFeatureArgVal(models.Model):
    '''
    Created on 13 de ago de 2017

    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    Argumentos (i.e. parametros) usados para instanciar esta feature 
    '''
    nam_argument = models.CharField(max_length=45)
    val_argument = models.CharField(max_length=45)
    
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