from grafo import Grafo

class reciprocidade(Grafo):
    def compute_feature(self,index,grafo):
            cont = 0
            lista = grafo.getverticesaidas(index)
            for dados in lista:
                if(index in grafo.getverticesaidas(dados)):
                    cont+=1
                else:
                    pass
            return cont 