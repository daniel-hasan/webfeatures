'''
Created on 2 de Out de 2018

@author: Rubio Torres Castro Viana <rubiotorres15@gmail.com>
'''
"""
    Classe Clusterizacao:
    Classe para produzir o coeficiente de Clusterizacao de um vertice:
        Metodos:
            compute_feature: Corrigir!!!
"""

from feature.GraphBasedFeature import *

class Clusterizacao(GraphBasedFeature):
    def __init__(name,description,reference,visibility,text_format,feature_time_per_document,distanciaMax):
        super().__init__(self,name,description,reference,visibility,text_format,feature_time_per_document)
        self.distanciaMax = distanciaMax

    def compute_feature(self,grafo):
        dicresult={}
        for index in range(0,len(grafo.getvertices())):
            cont = 0
            lista = grafo.get_vertices_saida(index)
            for dados in lista:
                for li in grafo.get_vertices_saida(dados):
                    if(li in lista):
                        cont+=1
                    else:
                        pass
            print cont
            if(cont != 0):
                dicresult[index] =len(lista)/cont
            else:
                dicresult[index] = 0
        return dicresult
