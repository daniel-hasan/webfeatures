from grafo import*
from clustering import *
from reciprocidade import *
from pgrank import *
from rge import *
from rgs import *
from raee import *
from raes import *
from rase import *

'''
Created on 26 de Set de 2018
@author: Rubio Torres Castro Viana <rubiotorres15@gmail.com>
'''
""" 
    Classe LeitorArestaarquivo:
    Classe para ler arestas de arquivos
        Metodos:
            __init__: Classe inicial que abre o arquivo
            Le_aresta: Nome Le linha a linha e retorna uma tupla <x,y> 
            Fechar: Fecha o arquivo
"""

class LeitorArestaArquivo(LeitorAresta):
    def __init__(self,arquivo):
        self.pointer = open(arquivo,"r")
    
    def le_aresta(self):
        str_line = self.pointer.readline()
        if(not str_line):
            return None
        str_line = str_line.strip('\n')
        return str_line.split(',')


    def fechar(self):
        self.pointer.close()

""" 
    Classe Grafoarquivo:
    Classe para criar grafos de arquivo
        Metodos:
            __init__: 
                Possui arestas[] para armazenar todos os arestas no formato:
                    <[x,y],[x,y],[x,y]  
                Possui vertices[] para armazenar os vetices unicos no formato:
                    <x,y,z,w>
            extraiarestas: Extrai arestas do arquivo e chama adicionaaresta
            adicionaAresta: Adiciona arestas do tipo <x,y> na lista de arestas
            getverticesaidas: lista todos os vertices que saem de um vertice
            getverticesentrada: lista todos os vertices que entram em um vertice
            getvertices: Retorna todos os vertices
            getvertice: Retorna o vertice de certo index
"""
class grafolistaadjacencia(Grafo):
    lista_adjacencia = []
    lista_incidencia = []
    vertices = []
    def __init__(self,leitor_aresta):
        self.extraiarestas(leitor_aresta)
    def extraiarestas(self,leitor_aresta):
        line = leitor_aresta.le_aresta()        
        while  line != None:
            self.adicionaAresta(line[0],line[1])
            line = leitor_aresta.le_aresta()
        leitor_aresta.fechar()

    def adicionaAresta(self,de_nodo,para_nodo):
        if((de_nodo in self.vertices) == False):
            self.vertices.append(de_nodo)
            self.lista_adjacencia.append([])
            self.lista_incidencia.append([])
        if((para_nodo in self.vertices) == False):
            self.vertices.append(para_nodo)
            self.lista_adjacencia.append([])
            self.lista_incidencia.append([])
        self.lista_adjacencia[self.vertices.index(de_nodo)].append(self.vertices.index(para_nodo))        
        self.lista_incidencia[self.vertices.index(para_nodo)].append(self.vertices.index(de_nodo))
    def get_vertices_saida(self,index):
        return self.lista_adjacencia[index]  
    def get_vertices_entrada(self,index):
        return self.lista_incidencia[index]  
    def getvertices(self):
        return self.vertices
    def getvertice(self,index):
        return self.vertices[index] 
    def get_vertice_ids(self):
        vertices = []
        for entrada in self.vertices:
            vertices.append(self.vertices.index(entrada))
        return vertices



if __name__ == "__main__":
    arquivo = LeitorArestaArquivo("grafo_mini.txt")
    artigo = grafolistaadjacencia(arquivo)
    print artigo.get_vertices_entrada(0)
    ran = AssortatividadeSaidaEntrada()
    print ran.compute_feature(artigo)
