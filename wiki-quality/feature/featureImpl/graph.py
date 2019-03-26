from feature import GraphBasedFeature
class Indegree(GraphBasedFeature):
        def compute_feature(self,graph):
                dic_result = {}
                for vertice_id in graph.get_vertice_ids():
                        dic_result[vertice_id] = len(graph.get_vertices_entrada(vertice_id))
                return dic_result

class Outdegree(GraphBasedFeature):
    def compute_feature(self,grafo):
        dicresult = {}
        for index in range(0,len(grafo.getvertices())):
            dicresult[index] = len(grafo.get_vertices_saida(index))
        return dicresult

class AssortativeInputInput (GraphBasedFeature):
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

class AssortativeInputOutput(GraphBasedFeature):
    def compute_feature(self,graph):
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

class AssortativeOutputInput(GraphBasedFeature):
    def compute_feature(self,graph):
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

class pageRank(GraphBasedFeature):
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
            #print (ranka.items())
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

class Reciprocity(GraphBasedFeature):
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
            if (len(lista) != 0):
                dicresult[index] = cont/len(lista)
            else:
                dicresult[index] = 0
        return dicresult

class Clusterizacao(GraphBasedFeature):
    def compute_feature(self,grafo):
        dicresult={}
        for index in range(0,len(grafo.getvertices())):
            number = 0
            degree = len(grafo.get_vertices_saida(index))
            lista = grafo.get_vertices_saida(index)
            for dados in lista:
                for li in grafo.get_vertices_saida(dados):
                    if(li in lista):
                        number+=1
                    else:
                        pass
            if(degree != 0):
                dicresult[index] =number/degree*(degree-1)
            else:
                dicresult[index] = 0
        return dicresult
