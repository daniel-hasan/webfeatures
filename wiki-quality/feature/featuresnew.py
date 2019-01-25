class features():
    def rgs(self,index,grafo):
        return len(grafo.getverticesaidas(index))
    def rge(self,index,grafo):
        return len(grafo.getverticesentrada(index))
    def clustering(self,index,grafo):
        cont = 0
        lista = grafo.getverticesaidas(index)
        for dados in lista:
            for li in grafo.getverticesaidas(dados):
                if(li in lista):
                    cont+=1
                else:
                    pass
        return len(lista)/cont
    def reciprocidade(self,index,grafo):
        cont = 0
        lista = grafo.getverticesaidas(index)
        for dados in lista:
            if(index in grafo.getverticesaidas(dados)):
                cont+=1
            else:
                pass
        return cont 