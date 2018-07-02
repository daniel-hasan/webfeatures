# -*- coding: utf-8 -*-
'''
Created on 8 de ago de 2017

@author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
Classes que podem ser uteis nos modelos do app wqual
'''
from abc import abstractstaticmethod
from django.db import models
#from django.db.models import SubfieldBase
from django.db.models.deletion import ProtectedError

from utils.basic_entities import FormatEnum

import base64, bz2, lzma


#from wqual.models.utils import EnumModel
class EnumQuerySet(models.query.QuerySet):
    def get(self, **kwargs):
        try:
            return super().get(**kwargs)
        except self.model.DoesNotExist:
            self.update_enums_in_db()
            return super().get(**kwargs)
    def has_enum_in_db(self,enum):
        '''
        Created on 15 de ago de 2017

        @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
        Busca se um determinado enum existe no BD pelo seu nome.
        '''
        return self.filter(name=enum.name).exists()

    def get_enum(self,enum):
        '''
        Created on 16 de nov de 2017

        @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
        Retorna o enum
        '''
        return self.get(name=enum.name)

    def insert_enum(self,enum):
        '''
        Created on 15 de ago de 2017

        @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
        Insere um enum no BD
        '''
        ModelClass = self.model
        obj = ModelClass(name=enum.name,value=enum.value)
        obj.save()

    def update_enums_in_db(self):
        '''
        Created on 15 de ago de 2017

        @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>

        Efetua a atualização dos valores/nomes dos enuns se necessário:
        -> Deleta as instancias que estão no BD mas nao no Enum correspondente
        -> Atualiza as instancias que estão no BD mas com valores (value) diferentes
        -> Insere as instancias que estão no Enum e não no BD
        '''
        EnumClass = self.model.get_enum_class()

        #deleta as instancias que estao no bd e não estao no enum
        for obj in self.all():
            if not isinstance(obj,EnumModel):
                raise TypeError("A class"+str(self.model)+" deve ser subclasse de EnumModel para poder usar o EnumManager!")

            if not obj.has_instance_in_enum():
                try:
                    obj.delete()
                except ProtectedError as p_error:
                    str_erro = "A instancia de valor'{instancia}' no banco de dados do enum  '{enum_class}' não pode ser excluída por ela possuir referencias com outras tabelas. Erro no django:  {erro}".format(erro=str(p_error),enum_class=str(EnumClass),instancia=str(obj))
                    raise ProtectedError(str_erro,protected_objects=p_error.protected_objects)
            else:
                #verifica se o enum desta instancia está com o valor correto
                #caso não esteja, atualiza no banco de dados
                enum_obj = obj.get_enum()
                if(enum_obj.value != obj.value):
                    obj.value = enum_obj.value
                    obj.save()

        #insere no bd as instancias que estao no enum e nao estao no bd
        for enum in EnumClass:
            if not self.has_enum_in_db(enum):
                self.insert_enum(enum)


class EnumManager(models.Manager.from_queryset(EnumQuerySet)):
    '''
    Created on 15 de ago de 2017

    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    Classe com os métodos para atualizar automaticamente um Enum em um banco de dados.
    '''






    def get_queryset(self):
        '''
        Created on 15 de ago de 2017

        @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
        Atualiza os enuns sempre quando esta classe de modelo
        for consultada pela primeira vez durante a execução do app.
        '''
        if(not hasattr(self.model, '__first_query') ):
            #print("Prima vez")
            setattr(self.model,"__first_query", False)
            self.update_enums_in_db()


        return super(EnumManager, self).get_queryset()

class EnumModel(models.Model):
    '''
    Created on 15 de ago de 2017

    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    Classe abstrata que armazena os atributos comuns aos Enuns (name e value).
    O enum é representado por uma igualdade x = y em que x é o nome e y é o valor.
    '''
    name = models.CharField(max_length=45,unique=True)
    value = models.CharField(max_length=255)
    objects = EnumManager()

    @staticmethod
    @abstractstaticmethod
    def get_enum_class():
        '''
        Created on 15 de ago de 2017

        @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>

        Método que obtem a classe correspondente deste Enum
        '''
        raise NotImplementedError("Voce deve criar uma subclasse e a mesma deve sobrepor este método")




    def has_instance_in_enum(self):
        '''
        Created on 15 de ago de 2017

        @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>

        Verifica se a instancia atual existe no enum
        '''
        try:
            self.get_enum()
        except KeyError:
            return False

        return True

    def get_enum(self):
        '''
        Created on 15 de ago de 2017

        @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>

        Obtem o Enum
        '''
        EnumClass = self.get_enum_class()
        return EnumClass[self.name]

    def __str__(self):
        return "{name}: {value} ({id})".format(id=self.id,name=self.name,value=self.value)

    class Meta:
        abstract = True

class Format(EnumModel):
    '''
    Created on 14 de ago de 2017

    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    Armazena os possíveis formatos de arquivo (de acordo com o enum FormatEnum)
    '''

    @staticmethod
    def get_enum_class():
        return FormatEnum
    def __str__(self):
        return self.value
    
class CompressedTextField(models.TextField):

    #__metaclass__ = models.SubfieldBase  #Algumas versoes django nao aceitam Subfield
    def to_python(self, value):
        if not value:
            print("int")
            return value

        try:
            return lzma.compress(bytes(value, 'utf-8'))

        except Exception:
            return value

    def get_prep_value(self, value):
        if not value:
            return value

        try:
            value.decode('base64')
            return value
        except Exception:
            try:
                tmp = lzma.decompress(value).decode('utf-8')
                print("tmp")
                print(tmp)
            except Exception:
                return value
            else:
                if len(tmp) > len(value):
                    return value
                return tmp
