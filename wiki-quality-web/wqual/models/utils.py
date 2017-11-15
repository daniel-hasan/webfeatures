# -*- coding: utf-8 -*-
'''
Created on 8 de ago de 2017

@author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
Classes que podem ser uteis nos modelos do app wqual
'''
from abc import abstractstaticmethod
 
from django.db import models
from django.db.models.deletion import ProtectedError

class EnumManager(models.Manager):
    '''
    Created on 15 de ago de 2017
    
    @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
    Classe com os métodos para atualizar automaticamente um Enum em um banco de dados. 
    '''

    
    def has_enum_in_db(self,enum):
        '''
        Created on 15 de ago de 2017
        
        @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
        Busca se um determinado enum existe no BD pelo seu nome.
        '''
        return self.filter(name=enum.name).exists()
    
    def insert_enum(self,enum):
        '''
        Created on 15 de ago de 2017
        
        @author: Daniel Hasan Dalip <hasan@decom.cefetmg.br>
        Insere um enum no BD
        '''
        ModelClass = self.model
        obj = ModelClass(name=enum.name,value=enum.value)
        obj.save()
    
  
    
    
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

