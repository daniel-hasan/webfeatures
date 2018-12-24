from feature.features import GraphBasedFeature

'''
Created on 9 de Out de 2018

@author: Rubio Torres Castro Viana <rubiotorres15@gmail.com>
'''
""" 
    Classes com as features

"""
class GrauSaida(GraphBasedFeature):
    def compute_feature(self,grafo):
        dicresult = {}
        for index in range(0,len(grafo.getvertices())):
            dicresult[index] = len(grafo.get_vertices_saida(index))
        return dicresult 

class GrauEntrada(GraphBasedFeature):
    def compute_feature(self,grafo):
        dicresult={}
        for index in range(0,len(grafo.getvertices())):
            dicresult[index] = len(grafo.get_vertices_entrada(index))
        return dicresult 
class PgRank(GraphBasedFeature):
    rank = {}
    def __init__(self,dumping_factor,convergencia):
        self.convergencia=convergencia
        self.dumping_factor=dumping_factor
    def compute_feature(self,grafo):
        for cont in range(0,len(grafo.getvertices())):
            self.rank[cont] = (1-self.dumping_factor)
        self.atualizar(grafo,self.rank)
        return self.rank
    def atualizar(self,grafo,ran,):
        ranka = ran
        norma = sum(ran)
        for index in range(0,len(ran)):
            cont=0
            for entrada in grafo.get_vertices_entrada(index):
                cont+=ran[entrada]/len(grafo.get_vertices_saida(entrada))
            ranka[index]=((1-0.85) + 0.85 * cont)/norma
        s=sum(ran)-sum(ranka)
        if(abs(s)<self.convergencia):
            self.rank=ranka
        else:
            self.atualizar(grafo,ranka)        

class Clusterizacao(GraphBasedFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document,distanciaMax):
        super().__init__(self,name,description,reference,visibility,text_format,feature_time_per_document)
        self.distanciaMax = distanciaMax

    def compute_feature(self,grafo):
        dicresult={}
        for index in range(0,len(grafo.getvertices())):
            cont = 0
            lista = grafo.get_vertices_saida(index)
            for dados in lista:
                for li in grafo.get_vertices_saida(dados):
                    if(li in lista):
                        cont+=1
                    else:
                        pass
            print cont
            if(cont != 0):
                dicresult[index] =len(lista)/cont
            else:
                dicresult[index] = 0
        return dicresult

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

            media = soma/len(listaVizinhos)
            dic_result[vertice_id] = dic_result[vertice_id]/media
        return dic_result

class AssortatividadeEntradaSaida(GraphBasedFeature):
    """
        Para cada vertice v, o grauEntrada(v) dividido
        pela media do grau de saida dos vizinhos
            raes = rge/avgGrauSaida
    """
    def compute_feature(self,graph):
        dic_result = {}
        for vertice_id in graph.get_vertice_ids():
            dic_result[vertice_id] = len(graph.get_vertices_entrada(vertice_id))
            #dividir pela media do grau de saida dos vizinhos
            soma = 0
            listaVizinhos = graph.get_vertices_saida(vertice_id)
            for vertice_id_saida in listaVizinhos:
                soma += len(graph.get_vertices_saida(vertice_id_saida))

            media = soma/len(listaVizinhos)
            dic_result[vertice_id] = dic_result[vertice_id]/media
        return dic_result

class AssortatividadeSaidaEntrada (GraphBasedFeature):
    def compute_feature(self,graph):
        dic_result = {}
        for vertice_id in graph.get_vertice_ids():
            dic_result[vertice_id] = len(graph.get_vertices_saida(vertice_id))
            #dividir pela media do grau de entrada dos vizinhos
            soma = 0
            listaVizinhos = graph.get_vertices_saida(vertice_id)
            for vertice_id_saida in listaVizinhos:
                soma = soma+len(graph.get_vertices_entrada(vertice_id_saida))

            media = soma/len(listaVizinhos)
            dic_result[vertice_id] = dic_result[vertice_id]/media
        return dic_result

class AssortatividadeSaidaSaida (GraphBasedFeature):
    def compute_feature(self,graph):
        dic_result = {}
        for vertice_id in graph.get_vertice_ids():
            dic_result[vertice_id] = len(graph.get_vertices_saida(vertice_id))
            #dividir pela media do grau de saida dos vizinhos
            soma = 0
            listaVizinhos = graph.get_vertices_saida(vertice_id)
            for vertice_id_saida in listaVizinhos:
                soma = soma+len(graph.get_vertices_saida(vertice_id_saida))

            media = soma/len(listaVizinhos)
            dic_result[vertice_id] = dic_result[vertice_id]/media
        return dic_result

class Reciprocidade(GraphBasedFeature):
    def compute_feature(self,grafo):
        dicresult = {}
        for index in range(0,len(grafo.getvertices())):
            cont = 0
            lista = grafo.get_vertices_saida(index)
            for dados in lista:
                if(index in grafo.get_vertices_saida(dados)):
                    cont+=1
                else:
                    pass
            if(len(lista)==0):
                dicresult[index] = 0
            else:
                dicresult[index] = cont/len(lista)
        return dicresult