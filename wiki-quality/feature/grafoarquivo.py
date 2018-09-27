from grafo import*
""" 
    Classe LeitorArestaarquivo:
    Classe para ler arestas de arquivos
        Metodos:
            __init__: Classe inicial que abre o arquivo
            Le_aresta: Nome Le linha a linha e retorna uma tupla <x,y> 
            Fechar: Fecha o arquivo
"""

class LeitorArestaArquivo(LeitorAresta):
    def __init__(self,arquivo):
        self.pointer = open(arquivo,"r")
    
    def le_aresta(self):
        str_line = self.pointer.readline()
        if(not str_line):
            return None
        str_line = str_line.strip('\n')
        return str_line.split(',')


    def fechar(self):
        self.pointer.close()

""" 
    Classe Grafoarquivo:
    Classe para criar grafos de arquivo
        Metodos:
            __init__: 
                Possui arestas[] para armazenar todos os arestas no formato:
                    <[x,y],[x,y],[x,y]  
                Possui vertices[] para armazenar os vetices unicos no formato:
                    <x,y,z,w>
            extraiarestas: Extrai arestas do arquivo e chama adicionaaresta
            adicionaAresta: Adiciona arestas do tipo <x,y> na lista de arestas
            getverticesaidas: lista todos os vertices que saem de um vertice
            getverticesentrada: lista todos os vertices que entram em um vertice
            getvertices: Retorna todos os vertices
            getvertice: Retorna o vertice de certo index
"""
class Grafoarquivo(Grafo):
    lista_adjacencia = []
    lista_incidencia = []
    vertices = []
    arestas = []
    def __init__(self,leitor_aresta):
        self.extraiarestas(leitor_aresta)
    def extraiarestas(self,leitor_aresta):
        line = leitor_aresta.le_aresta()        
        while  line != None:
            tupla = []
            for nodo in line:
                tupla.append(nodo)
            self.adicionaAresta(tupla[0],tupla[1])
            line = leitor_aresta.le_aresta()
        leitor_aresta.fechar()
        self.lista_adjacencia = self.gerasaidas()
        self.lista_incidencia = self.gerasaidas()


    def adicionaAresta(self,de_nodo,para_nodo):
        line_aresta = []
        if((de_nodo in self.vertices) == False):
            self.vertices.append(de_nodo)
        if((para_nodo in self.vertices) == False):
            self.vertices.append(para_nodo)
        line_aresta.append(self.vertices.index(de_nodo))
        line_aresta.append(self.vertices.index(para_nodo))
        self.arestas.append(line_aresta)
    def gerasaidas(self):
        lista=[]
        for i in range(0,len(self.vertices)):
            vertice=[]
            for x in self.arestas:
                if i==x[0]:
                    vertice.append(x[1])
            lista.append(vertice)
        return lista
    def geraentrada(self):
        lista=[]
        for i in range(0,len(self.vertices)):
            vertice=[]
            for x in self.arestas:
                if i==x[1]:
                    vertice.append(x[0])
            lista.append(vertice)
        return lista
    def getverticesaidas(self,index):
        return self.lista_adjacencia[index]  
    def getverticesentrada(self,index):
        return self.lista_incidencia[index]  
    def getvertices(self):
        return self.vertices
    def getvertice(self,index):
        return self.vertices[index]  




if __name__ == "__main__":
    arquivo = LeitorArestaArquivo("grafo_mini.txt")
    artigo = Grafoarquivo(arquivo)
    print artigo.vertices
    print artigo.vertices
    print artigo.getverticesaidas(0)