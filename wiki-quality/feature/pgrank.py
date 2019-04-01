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
    def compute_feature(self,grafo):
        rank={}
        s=100
        d=0.85
        cont = len(grafo.getvertices())
        #Inicializacao
        while (cont > 0):
            rank[cont-1] = 1-d #Inicializa com 1-d
            cont=cont - 1
        while(abs(s)>0.1):
            ranka={}
            #Calculo do page rank
            for index in range(0,len(rank)):
                soma=0
                for entrada in grafo.get_vertices_entrada(index):
                    soma+=rank[entrada]/len(grafo.get_vertices_saida(entrada))
                ranka[index]= (1-d) + (d * soma)
            #normalizacao
            norma = sum(ranka.values())
            print (ranka.items())
            for cont,val_rank in ranka.items():
                #print("pos "+str(cont)+" valrank: "+str(val_rank))
                ranka[cont] = val_rank/norma
            #print (ranka)
            #calculo da convergencia
            s=sum(rank.values())-sum(ranka.values())
            #atualizacao do valor do page rank
            for i,val_rank in ranka.items():
                rank[i] = val_rank
        return rank
