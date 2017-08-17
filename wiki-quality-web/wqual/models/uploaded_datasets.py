# -*- coding: utf-8 -*-
'''
Created on 14 de ago de 2017

@author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
Tabelas relacionadas com o upload de datasets para a futura 
extração de features. 
As tabelas relacionadas com o resultado desta extração também está neste arquivo.
'''
from enum import IntEnum, Enum
from django.contrib.auth.models import User, Group
from django.db import models

from utils.basic_entities import FormatEnum
from wqual.models import FeatureSet
from wqual.models.utils import EnumModel, EnumManager


class StatusEnum(Enum):
    '''
    Created on 14 de ago de 2017
    
    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
Tipos de status da extração de features de um determinado dataset
    '''
    PROCESSING = "Processing"
    COMPLETE = "Completed"
    NOT_AVALIABLE = "The time to download the result has expired"

class Status(EnumModel):
    '''
    Created on 14 de ago de 2017
    
    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    Modelo para armazenar da extração de features
    '''
    
    @staticmethod
    def get_enum_class():
        return StatusEnum
    

class Format(EnumModel):
    '''
    Created on 14 de ago de 2017
    
    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    Armazena os possíveis formatos de arquivo (de acordo com o enum FormatEnum)
    '''
    
    @staticmethod
    def get_enum_class():
        return FormatEnum
    

        
class Dataset(models.Model):
    '''
    Created on 14 de ago de 2017
    
    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    Dataset que o usuário enviou
    '''
    nam_dataset = models.CharField(max_length=45)
    dat_submitted = models.DateTimeField()
    dat_valid_until = models.DateTimeField(blank=True, null=True)
    
    
    format = models.ForeignKey(Format, models.PROTECT)    
    
    feature_set = models.ForeignKey(FeatureSet, models.PROTECT)
    user = models.ForeignKey(User, models.PROTECT)
    status = models.ForeignKey(Status, models.PROTECT)


class ResultValityPerUserGroup(models.Model):
    '''
    Created on 16 de ago de 2017
    
    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    O resultado de um dataset tem prazo de validade variável considerando
    o grupo no qual o usuário que enviou o dataset pertence.
    '''
    num_days_valid = models.IntegerField()    
    
    user_group = models.ForeignKey(Group, models.PROTECT)


class Document(models.Model):
    '''
    Created on 14 de ago de 2017
    
    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    Cada documento contido no dataset que o usuário enviou
    '''

    nam_file = models.CharField(max_length=255, blank=True, null=True)
    
    dataset = models.ForeignKey(Dataset, models.PROTECT)
class DocumentText(models.Model):
    '''
    Created on 14 de ago de 2017
    
    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    Texto do documento
    '''
    dsc_text = models.TextField()
    document = models.OneToOneField(Document, models.PROTECT)
    
class DocumentResult(models.Model):
    '''
    Created on 14 de ago de 2017
    
    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    Resultado obtido do documento
    '''
    dsc_result = models.TextField()
    
    document = models.OneToOneField(Document, models.PROTECT)
    
    