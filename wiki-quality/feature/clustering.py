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

from GraphBasedFeature import *

class Clusterizacao(GraphBasedFeature):
    def compute_feature(self,index,grafo):
            cont = 0
            lista = grafo.getverticesaidas(index)
            for dados in lista:
                for li in grafo.getverticesaidas(dados):
                    if(li in lista):
                        cont+=1
                    else:
                        pass
            return len(lista)/cont