from grafo import Grafo

class Grausaida(Grafo):
    def compute_feature(self,index,grafo):
        return len(grafo.getverticesentrada(index))