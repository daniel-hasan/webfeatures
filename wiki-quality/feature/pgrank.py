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
from GraphBasedFeature import *
class pgrank(GraphBasedFeature):
    rank = []
    def compute_feature(self,grafo):
        cont = len(grafo.getvertices())
        while cont > 0:
            self.rank.insert((cont-1),0.15)
            cont=cont - 1
        self.atualizar(grafo,self.rank)

        return self.rank
    def atualizar(self,grafo,ran):
        ranka = ran[:]
        norma = sum(ran)
        for index in range(0,len(ran)):
            cont=0
            for entrada in grafo.getverticesentrada(index):
                cont+=ran[entrada]/len(grafo.getverticesaidas(entrada))
            ranka[index]=((1-0.85) + 0.85 * cont)/norma
        s=sum(ran)-sum(ranka)
        if(abs(s)<0.1):
            self.rank=ranka[:]
        else:
            self.atualizar(grafo,ranka)        
        