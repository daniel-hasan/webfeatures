from grafo import Grafo

class GrauEntrada(Grafo):
    def compute_feature(self,index,grafo):
        return len(grafo.getverticesaidas(index))