""" 
    Classe LeitorAresta:
    Classe abstrata para ler arestas
        Metodos:
            Le_aresta: Nome auto descritivo 
"""

class LeitorAresta():
    #@abstractmethod
    def le_aresta(self):
        pass
    #@abstractmethod
    def fechar(self):
        pass

""" 
    Classe Grafo:
    Classe abstrata para criar grafos
        Metodos:
            __init__: 
                Possui arestas[] para armazenar todos os arestas no formato:
                    <[x,y],[x,y],[x,y]  
                Possui vertices[] para armazenar os vetices unicos no formato:
                    <x,y,z,w>
            adicionaAresta: Adiciona arestas
            getverticesaidas: Gera todos os vertices que saem de um vertice
            getverticesentrada: Gera todos os vertices que entram em um vertice
            getvertices: Retorna todos os vertices
            getvertice: Retorna o vertice de certo index
"""

class Grafo():

    def __init__(self,leitor_aresta):
        self.vertices = []
        self.arestas = []
        for de_nodo,para_nodo in leitor_aresta.le_aresta():
            self.adicionaAresta(de_nodo,para_nodo)
        leitor_aresta.fechar



    #@abstractmethod
    def adicionaAresta(self,de_nodo,para_nodo):
        pass 
    #@abstractmethod
    def getverticesaidas(self):
        pass  
    #@abstractmethod
    def getverticesentrada(self):
        pass
    #@abstractmethod
    def getvertices(self):
        pass
    #@abstractmethod
    def getvertice(self,index):
        pass

