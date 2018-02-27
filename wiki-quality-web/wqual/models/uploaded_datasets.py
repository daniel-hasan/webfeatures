# -*- coding: utf-8 -*-
'''
Created on 14 de ago de 2017

@author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
Tabelas relacionadas com o upload de datasets para a futura 
extração de features. 
As tabelas relacionadas com o resultado desta extração também está neste arquivo.
'''

from enum import IntEnum, Enum
import lzma

from django.contrib.auth.models import User, Group
from django.db import models, transaction

from utils.uncompress_data import CompressedFile
from wqual.models import FeatureSet, Format
from wqual.models.exceptions import FileSizeException
from wqual.models.utils import EnumModel, EnumManager, CompressedTextField


class StatusEnum(Enum):
    '''
    Created on 14 de ago de 2017
    
    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
Tipos de status da extração de features de um determinado dataset
    '''
    SUBMITTED = "Submitted"
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
    
   
class Dataset(models.Model):
    '''
    Created on 14 de ago de 2017
    
    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    Dataset que o usuário enviou
    '''
    nam_dataset = models.CharField(max_length=45)
    
    dat_submitted = models.DateTimeField()
    dat_valid_until = models.DateTimeField(blank=True, null=True)
    
    start_dat_processing = models.DateTimeField(blank=True, null=True)
    end_dat_processing = models.DateTimeField(blank=True, null=True)
    
    format = models.ForeignKey(Format, models.PROTECT)    
    
    feature_set = models.ForeignKey(FeatureSet, models.PROTECT)
    user = models.ForeignKey(User, models.PROTECT)
    status = models.ForeignKey(Status, models.PROTECT)
    dsc_result_header = models.TextField(blank=True, null=True)
    
    num_proc_extractor = models.IntegerField(blank=True, null=True)
         
    def save_compressed_file(self,comp_file_pointer):
            #validacao ser feita aqui
            
            #se um dos arquivos for maior que XX, 
            #lancar uma excecao falando que o tamanho foi maior
            
            
            #inserção
            #save
            objFileZip = CompressedFile.get_compressed_file(comp_file_pointer)
            
            int_limit = 50*(1024*1024)
            for name,int_file_size in objFileZip.get_each_file_size():
                if int_file_size > int_limit:
                    raise FileSizeException("The file "+name+" exceeds the limit of "+str(int_limit)+" bytes")
                
            self.save()
            i = 0   
            for name,strFileTxt in objFileZip.read_each_file():
                with transaction.atomic():
                    i = i+1
                    print(name+": "+str(i))
                    if(name == "1095706.html"):
                        a=1
                        a = a+1
                        pass
                    objDocumento = Document(nam_file=name,dataset=self)
                    objDocumento.save()
                    objDocumentoTexto = DocumentText(document=objDocumento,dsc_text=strFileTxt)
                    objDocumentoTexto.save()
                    self.document_set.add(objDocumento,bulk=False)
                

                
                
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
    dataset = models.ForeignKey(Dataset, models.CASCADE)
    
    
    
class DocumentText(models.Model):
    '''
    Created on 14 de ago de 2017
    
    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    Texto do documento
    '''
    dsc_text_bin = models.BinaryField()    
    document = models.OneToOneField(Document, models.CASCADE)
    
    @property
    def dsc_text(self):
        return lzma.decompress(self.dsc_text_bin).decode("utf-8")

    @dsc_text.setter
    def dsc_text(self, dsc_result):
        dsc_text_bytes = bytes(str(dsc_result), 'utf-8')        
        self.dsc_text_bin = lzma.compress(dsc_text_bytes)    
class DocumentResult(models.Model):
    '''
    Created on 14 de ago de 2017
    
    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    Resultado obtido do documento
    '''
    dsc_result = models.TextField()
    document = models.OneToOneField(Document, models.CASCADE)

   
   
   