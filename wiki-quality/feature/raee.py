'''
@author: Larisse Stefany Pires Amorim <larisseamorim.mg@gmail.com>
'''
"""
    Classe AssortatividadeEntradaEntrada:
    Classe para produzir o Assortatividade de Entrada Entrada de um vertice:
        Metodos:
            compute_feature: Retorna a Assortatividade de entrada entrada de cada vértice
"""

from feature.GraphBasedFeature import *

class AssortatividadeEntradaEntrada (GraphBasedFeature):
def compute_feature(self,graph):
    dic_result = {}
    for vertice_id in graph.get_vertice_ids():
        dic_result[vertice_id] = len(graph.get_vertices_entrada(vertice_id))
        #dividir pela media do grau de entrada dos vizinhos
        soma = 0
        listaVizinhos = graph.get_vertices_saida(vertice_id)
        for vertice_id_saida in listaVizinhos:
            soma += len(graph.get_vertices_entrada(vertice_id_saida))
        if (len(listaVizinhos) == 0):
            media = 0
            dic_result[vertice_id] = 0
        else:
            media = soma/len(listaVizinhos)
            dic_result[vertice_id] = dic_result[vertice_id]/media
    return dic_result
