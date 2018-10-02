'''
Created on 2 de Out de 2018

@author: Rubio Torres Castro Viana <rubiotorres15@gmail.com>
'''
""" 
    Classe Reciprocidade:
    Classe para produzir o coeficiente de reciprocidade de um vertice:
        Metodos:
            compute_feature: Retorna a quantidade de vertice que tambem tem uma ligação de volta com o vertice origem
"""
from GraphBasedFeature import *

class reciprocidade(GraphBasedFeature):
    def compute_feature(self,index,grafo):
            cont = 0
            lista = grafo.getverticesaidas(index)
            for dados in lista:
                if(index in grafo.getverticesaidas(dados)):
                    cont+=1
                else:
                    pass
            return cont 