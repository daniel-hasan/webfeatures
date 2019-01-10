'''
@author: Larisse Stefany Pires Amorim <larisseamorim.mg@gmail.com>
'''
"""
    Classe AssortatividadeSaidaEntrada:
    Classe para produzir o Assortatividade de Saída Saída de um vertice:
        Metodos:
            compute_feature: Retorna a Assortatividade de saida saida de cada vértice
"""

from feature.GraphBasedFeature import *
class AssortatividadeSaidaEntrada (GraphBasedFeature):
    def compute_feature(self,graph):
        dic_result = {}
        for vertice_id in graph.get_vertice_ids():
            dic_result[vertice_id] = len(graph.get_vertices_saida(vertice_id))
            #dividir pela media do grau de saida dos vizinhos
            soma = 0
            listaVizinhos = graph.get_vertices_saida(vertice_id)
            for vertice_id_saida in listaVizinhos:
                soma = soma+len(graph.get_vertices_saida(vertice_id_saida))
            if (soma != 0):
                media = soma/len(listaVizinhos)
                dic_result[vertice_id] = dic_result[vertice_id]/media
            else:
                 dic_result[vertice_id] = 0
        return dic_result
