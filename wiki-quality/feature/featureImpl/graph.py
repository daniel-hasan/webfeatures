from feature import GraphBasedFeature
from feature.features import *

class Indegree(GraphBasedFeature):
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):

        self.name = name
        self.description = description
        self.reference = reference
        self.visibility = visibility
        self.text_format = text_format
        self.feature_time_per_document = feature_time_per_document
        self.arr_configurable_param = []
    
    def compute_feature(self, graph):
            dic_result = {}
            for vertice_id in graph.get_vertice_ids():
                    dic_result[vertice_id] = len(graph.get_vertices_entrada(vertice_id))
            return dic_result

class Outdegree(GraphBasedFeature):
    
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):

        self.name = name
        self.description = description
        self.reference = reference
        self.visibility = visibility
        self.text_format = text_format
        self.feature_time_per_document = feature_time_per_document
        self.arr_configurable_param = []
        
    def compute_feature(self, graph):
        dicresult = {}
        for index in range(0,len(graph.getvertices())):
            dicresult[index] = len(graph.get_vertices_saida(index))
        return dicresult

class AssortativeInputInput(GraphBasedFeature):
    
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):

        self.name = name
        self.description = description
        self.reference = reference
        self.visibility = visibility
        self.text_format = text_format
        self.feature_time_per_document = feature_time_per_document
        self.arr_configurable_param = []
        
    def compute_feature(self, graph):
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

class AssortativeInputOutput(GraphBasedFeature):
    
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):

        self.name = name
        self.description = description
        self.reference = reference
        self.visibility = visibility
        self.text_format = text_format
        self.feature_time_per_document = feature_time_per_document
        self.arr_configurable_param = []
        
    def compute_feature(self, graph):
        dic_result = {}
        for vertice_id in graph.get_vertice_ids():
            dic_result[vertice_id] = len(graph.get_vertices_entrada(vertice_id))
            #dividir pela media do grau de saida dos vizinhos
            soma = 0
            listaVizinhos = graph.get_vertices_saida(vertice_id)
            for vertice_id_saida in listaVizinhos:
                soma += len(graph.get_vertices_saida(vertice_id_saida))
            if (soma != 0):
                media = soma/len(listaVizinhos)
                dic_result[vertice_id] = dic_result[vertice_id]/media
            else:
                dic_result[vertice_id] = 0
        return dic_result

class AssortativeOutputOutput(GraphBasedFeature):
    
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):

        self.name = name
        self.description = description
        self.reference = reference
        self.visibility = visibility
        self.text_format = text_format
        self.feature_time_per_document = feature_time_per_document
        self.arr_configurable_param = []
        
    def compute_feature(self, graph):
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

class AssortativeOutputInput(GraphBasedFeature):
    
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):

        self.name = name
        self.description = description
        self.reference = reference
        self.visibility = visibility
        self.text_format = text_format
        self.feature_time_per_document = feature_time_per_document
        self.arr_configurable_param = []
        
    def compute_feature(self, graph):
        dic_result = {}
        for vertice_id in graph.get_vertice_ids():
            dic_result[vertice_id] = len(graph.get_vertices_saida(vertice_id))
            #dividir pela media do grau de entrada dos vizinhos
            soma = 0
            listaVizinhos = graph.get_vertices_saida(vertice_id)
            for vertice_id_saida in listaVizinhos:
                soma = soma+len(graph.get_vertices_entrada(vertice_id_saida))
            if (soma != 0):
                media = soma/len(listaVizinhos)
                dic_result[vertice_id] = dic_result[vertice_id]/media
            else:
                dic_result[vertice_id] = 0
        return dic_result

class PageRank(GraphBasedFeature):
    
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document, damping_factor=0.85,convergence=0.01):
        self.name = name
        self.description = description
        self.reference = reference
        self.visibility = visibility
        self.text_format = text_format
        self.feature_time_per_document = feature_time_per_document
        self.arr_configurable_param = []
        self.damping_factor = damping_factor
        self.convergence =convergence
        
    def compute_feature(self,grafo):
        rank={}
        s=self.convergence
        d=self.damping_factor
        cont = len(grafo.getvertices())
        #Inicializacao
        while (cont > 0):
            rank[cont-1] = 1-d #Inicializa com 1-d
            cont=cont - 1
        while(abs(s)>0.1):
            ranka={}
            #Calculo do PageRank
            for index in range(0,len(rank)):
                soma=0
                for entrada in grafo.get_vertices_entrada(index):
                    soma+=rank[entrada]/len(grafo.get_vertices_saida(entrada))
                ranka[index]= (1-d) + (d * soma)
            #normalizacao
            norma = sum(ranka.values())
            #print (ranka.items())
            for cont,val_rank in ranka.items():
                #print("pos "+str(cont)+" valrank: "+str(val_rank))
                ranka[cont] = val_rank/norma
            #print (ranka)
            #calculo da convergencia
            s=sum(rank.values())-sum(ranka.values())
            #atualizacao do valor do PageRank
            for i,val_rank in ranka.items():
                rank[i] = val_rank
        return rank

class Reciprocity(GraphBasedFeature):
    
    def __init__(self,name,description,reference,visibility,text_format,feature_time_per_document):

        self.name = name
        self.description = description
        self.reference = reference
        self.visibility = visibility
        self.text_format = text_format
        self.feature_time_per_document = feature_time_per_document
        self.arr_configurable_param = []
        
    def compute_feature(self, graph):
        dicresult = {}
        for index in range(0,len(graph.getvertices())):
            cont = 0
            lista = graph.get_vertices_saida(index)
            for dados in lista:
                if(index in graph.get_vertices_saida(dados)):
                    cont+=1
                else:
                    pass
            if (len(lista) != 0):
                dicresult[index] = cont/len(lista)
            else:
                dicresult[index] = 0
        return dicresult

class ClusteringCoefficient(GraphBasedFeature):
    
    def __init__(self, name, description, reference, visibility, text_format, feature_time_per_document, distance=1.0):

        self.name = name
        self.description = description
        self.reference = reference
        self.visibility = visibility
        self.text_format = text_format
        self.feature_time_per_document = feature_time_per_document
        self.arr_configurable_param = []
        self.distance = distance 

    def compute_feature(self,grafo):
        dicresult={}
        for index in range(0,len(grafo.getvertices())):
            number = 0
            degree = len(grafo.get_vertices_saida(index))
            lista = grafo.get_vertices_saida(index)
            for dados in lista:
                for li in grafo.get_vertices_saida(dados):
                    if(li in lista):
                        number +=1
                    else:
                        pass
            if(degree > 1):
                dicresult[index] =2*number/(degree*(degree-1))
            else:
                dicresult[index] = 0
        return dicresult
