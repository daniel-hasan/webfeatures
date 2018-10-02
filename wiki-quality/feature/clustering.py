from grafo import Grafo

class Clusterizacao(Grafo):
    def compute_feature(self,index,grafo):
            cont = 0
            lista = grafo.getverticesaidas(index)
            for dados in lista:
                for li in grafo.getverticesaidas(dados):
                    if(li in lista):
                        cont+=1
                    else:
                        pass
            return len(lista)/cont