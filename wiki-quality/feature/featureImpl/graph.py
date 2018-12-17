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

class pageRank(GraphBasedFeature):
    rank = {}
    def compute_feature(self,grafo):
        cont = len(grafo.getvertices())
        while cont > 0:
            self.rank[cont-1] = 0.15
            cont=cont - 1
        self.atualizar(grafo,self.rank)
        return self.rank
    def atualizar(self,grafo,ran):
        ranka = ran
        norma = sum(ran)
        for index in range(0,len(ran)):
            cont=0
            for entrada in grafo.get_vertices_entrada(index):
                cont+=ran[entrada]/len(grafo.get_vertices_saida(entrada))
            ranka[index]=((1-0.85) + 0.85 * cont)/norma
        s=sum(ran)-sum(ranka)
        if(abs(s)<0.1):
            self.rank=ranka
        else:
            self.atualizar(grafo,ranka)   

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
            dicresult[index] = cont 
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
            
            if(len(listaVizinhos) == 0):
                dic_result[vertice_id] = 0
            else: 
                media = soma/len(listaVizinhos)            
                dic_result[vertice_id] = dic_result[vertice_id]/media
        
        return dic_result

class AssortativeInputOutput (GraphBasedFeature):
    def compute_feature(self,graph):
        dic_result = {}
        for vertice_id in graph.get_vertice_ids():
            dic_result[vertice_id] = len(graph.get_vertices_entrada(vertice_id))
            #dividir pela media do grau de saida dos vizinhos
            soma = 0
            listaVizinhos = graph.get_vertices_saida(vertice_id)
            for vertice_id_saida in listaVizinhos:
                soma += len(graph.get_vertices_saida(vertice_id_saida))

            if(len(listaVizinhos) == 0):
                dic_result[vertice_id] = 0
            else: 
                media = soma/len(listaVizinhos)            
                dic_result[vertice_id] = dic_result[vertice_id]/media
        return dic_result

class AssortativeOutputInput (GraphBasedFeature):
    def compute_feature(self,graph):
        dic_result = {}
        for vertice_id in graph.get_vertice_ids():
            dic_result[vertice_id] = len(graph.get_vertices_saida(vertice_id))
            #dividir pela media do grau de saida dos vizinhos
            soma = 0
            listaVizinhos = graph.get_vertices_saida(vertice_id)
            for vertice_id_saida in listaVizinhos:
                soma = soma+len(graph.get_vertices_entrada(vertice_id_saida))
            
            if (len(listaVizinhos) == 0):
                dic_result[vertice_id] = 0;
            else:
                media = soma/len(listaVizinhos)
                dic_result[vertice_id] = dic_result[vertice_id]/media
                
        return dic_result

class AssortativeOutputOutput (GraphBasedFeature):
    def compute_feature(self,graph):
        dic_result = {}
        for vertice_id in graph.get_vertice_ids():
            dic_result[vertice_id] = len(graph.get_vertices_saida(vertice_id))
            #dividir pela media do grau de entrada dos vizinhos
            soma = 0
            listaVizinhos = graph.get_vertices_saida(vertice_id)
            for vertice_id_saida in listaVizinhos:
                soma = soma+len(graph.get_vertices_saida(vertice_id_saida))

            if (len(listaVizinhos) == 0):
                dic_result[vertice_id] = 0
            else:
                media = soma/len(listaVizinhos)
                dic_result[vertice_id] = dic_result[vertice_id]/media
                
        return dic_result
        
class Clustering (GraphBasedFEature):
    def comput_feature (self, graph):  
      def comput_feature (self, graph):       
        for vertice_id in graph.get_vertice_ids():
            visit = {}     
            fila = {}
            adj = {}
            visit.add(vertice_id)
            fila.add(vertice_id)
            dist = 0
            
        for vertice_id in fila:
           fila.remove(vertice_id)
           adj = graph.get_vertices_saida(vertice_id)
           for vertice in adj: 
               if (visit[vertice]):
                   dist = dist+1
                   visit.remove(vertice)
                   fila.add(vertice)
    
        return dist

            