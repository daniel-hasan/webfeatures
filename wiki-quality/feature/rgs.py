'''
Created on 2 de Out de 2018

@author: Rubio Torres Castro Viana <rubiotorres15@gmail.com>
'''
""" 
    Classe GrauSaida:
    Classe para produzir o grau de saida de um vertice:
        Metodos:
            compute_feature: retorna quantidade de vartices saida
"""
from GraphBasedFeature import *

class GrauSaida(GraphBasedFeature):
    def compute_feature(self,grafo):
        dicresult = {}
        for index in range(0,len(grafo.getvertices())):
            dicresult[index] = len(grafo.getverticesaidas(index))
        return dicresult 