'''
Created on 2 de Out de 2018

@author: Rubio Torres Castro Viana <rubiotorres15@gmail.com>
'''
""" 
    Classe pgrank:
    Classe para produzir o page rank do vertice:
        Metodos:
            compute_feature: ...
"""
from feature.GraphBasedFeature import *
class pgrank(GraphBasedFeature):
    rank = {}
    def compute_feature(self,grafo):
        s=100
        d=0.9
        cont = len(grafo.getvertices())
        while (cont > 0):
            self.rank[cont-1] = 1-d #Inicializa com 1-d
            cont=cont - 1
        while(abs(s)>=0.1):
            ranka = self.rank
            norma = sum(self.rank)
            for index in range(0,len(self.rank)):
                cont=0
                for entrada in grafo.get_vertices_entrada(index):
                    cont+=self.rank[entrada]/len(grafo.get_vertices_saida(entrada))
                ranka[index]=((1-d) + d * cont)/norma
            s=sum(self.rank)-sum(ranka)
            self.rank=ranka   
        