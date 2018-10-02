'''
Created on 2 de Out de 2018

@author: Rubio Torres Castro Viana <rubiotorres15@gmail.com>
'''
""" 
    Classe GrauEntrada:
        Classe para produzier o Graude entrada de um vertice
        Metodos:
            compute_feature: retorna grau de entrada
"""
from GraphBasedFeature import *

class GrauEntrada(GraphBasedFeature):
    def compute_feature(self,index,grafo):
        return len(grafo.getverticesentrada(index))