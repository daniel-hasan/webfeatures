from feature.graphImpl import *
import unittest

#Autor: Gabriel Gonçalves, 2020 (gabrielgoncalves310503@gmail.com)

class teste_leitorArquivo(unittest.TestCase):
    def testeLeitorArquivo(self):
        
        leitor = LeitorArestaArquivo("feature/tests/teste_grafo.csv")
        
        line = leitor.le_aresta()
        lista = []
        while line != None:
            lista.append(line)
            line = leitor.le_aresta()
            
        
        leitor.fechar()
        self.assertEqual(lista,[['A','C'],['A','B'],['B','C'],['C','A'],['C','B'],['D','B']])

        
if __name__ == "__main__":
    unittest.main()