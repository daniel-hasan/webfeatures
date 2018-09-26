""" 
    Classe LeitorAresta:
    Classe abstrata para ler arestas
        Metodos:
            Le_aresta: Nome auto descritivo 
"""
class LeitorAresta():
    def le_aresta(self):
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




    def adicionaAresta(self,de_nodo,para_nodo):
        pass 
    def getverticesaidas(self):
        pass  
    def getverticesentrada(self):
        pass
    def getvertices(self):
        pass
    def getvertice(self,index):
        pass

