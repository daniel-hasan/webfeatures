"""
        Para cada vertice v, é o grauEntrada(v) dividido
        pela média do grau de entrada dos vizinhos
            raee = rge/avgGrauEntrada
"""
class AssortatividadeEntradaEntrada (GraphBasedFeature):
    def compute_feature(graph):
        dic_result = {}
        for vertice_id in graph.get_vertice_ids():
            dic_result[vertice_id] = len(graph.get_vertices_entrada(vertice_id))
            #dividir pela media do grau de entrada dos vizinhos
            soma = 0
            listaVizinhos = graph.get_vertices_saida(vertice_id)
            for vertice_id_saida in listaVizinhos:
                soma += len(graph.get_vertices_entrada(vertice_id_saida))

            media = soma/len(listaVizinhos)
            dic_result[vertice_id] = dic_result[vertice_id]/media
        return dic_result
