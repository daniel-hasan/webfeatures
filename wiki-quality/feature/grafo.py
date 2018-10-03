from abc import abstractmethod
from featuresnew import*

'''
Created on 26 de Set de 2018

@author: Rubio Torres Castro Viana <rubiotorres15@gmail.com>
'''
""" 
    Classe LeitorAresta:
    Classe abstrata para ler arestas
        Metodos:
            Le_aresta: Nome auto descritivo 
"""

class LeitorAresta():
    @abstractmethod
    def le_aresta(self):
        pass
    @abstractmethod
    def fechar(self):
        pass

""" 
    Classe Grafo:
    Classe abstrata para criar grafos
        Metodos:
            __init__: 
                Possui arestas[] para armazenar todos os arestas no formato:
                    <[x,y],[x,y],[x,y]  
                Possui vertices[] para armazenar os vetices unicos no formato:
                    <x,y,z,w>
            adicionaAresta: Adiciona arestas
            getverticesaidas: Gera todos os vertices que saem de um vertice
            getverticesentrada: Gera todos os vertices que entram em um vertice
            getvertices: Retorna todos os vertices
            getvertice: Retorna o vertice de certo index
"""

class Grafo():
    @abstractmethod
    def __init__(self,leitor_aresta):
        pass
    @abstractmethod
    def adicionaAresta(self,de_nodo,para_nodo):
        pass 
    @abstractmethod
    def get_vertices_saida(self,index):
        pass  
    @abstractmethod
    def get_vertices_entrada(self,index):
        pass
    @abstractmethod
    def getvertices(self):
        pass
    @abstractmethod
    def getvertice(self,index):
        pass
    @abstractmethod
    def get_vertice_ids(self):
        pass

