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
    def compute_feature(self,grafo):
        dicresult={}        
        for index in range(0,len(grafo.getvertices())):
            number = 0
            degree = len(grafo.get_vertices_saida(index))
            lista = grafo.get_vertices_saida(index)
            for dados in lista:
                for li in grafo.get_vertices_saida(dados):
                    if(li in lista):
                        number+=1
                    else:
                        pass
            if(degree != 0):
                dicresult[index] =number/degree*(degree-1)
            else:
                dicresult[index] = 0
        return dicresult
