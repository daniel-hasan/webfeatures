from feature.featureImpl.graph import *
from feature.features import FeatureVisibilityEnum
from utils.basic_entities import FormatEnum,LanguageEnum,FeatureTimePerDocumentEnum
from feature.grafolistaadjacencia import grafolistaadjacencia
import unittest
class TestGraphFeatures(unittest.TestCase):
    def testFeatures(self):
        #o construtor possui os parametros pq são herdados de feature.features.FeatureCalculator (ver no arquivo feature/feature.py)
        #caso tenha mais elementos implementados (parametros) criar um novo construtor e chamar o super (ver classe Clusterizacao)
        arrFeaturesImplementadas = [Indegree("Indegree","Indegree Metric metric","reference", FeatureVisibilityEnum.public,
                                            FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS),
                                #Estes sao outros exemplos de instanciação, sao 3 tipos de coeficientes de clusterizacao que deverão ser testados
                                #Clusterizacao("Clustering coefficient","Description","reference", FeatureVisibilityEnum.public,
                                #        FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS,1),
                                #Clusterizacao("Clustering coefficient","Description","reference", FeatureVisibilityEnum.public,
                                #                                        FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS,2),
                                #Clusterizacao("Clustering coefficient","Description","reference", FeatureVisibilityEnum.public,
                                #                FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS,3),
                                ]
        #cria o grafo:
        grafo = grafolistaadjacencia()#essa classe irá mudar de nome - o Rubio irá mudar

        grafo.adicionaAresta("A","B")
        grafo.adicionaAresta("A","C")
        grafo.adicionaAresta("A","F")
        grafo.adicionaAresta("B","D")
        grafo.adicionaAresta("B","C")
        grafo.adicionaAresta("C","E")
        grafo.adicionaAresta("C","A")
        grafo.adicionaAresta("E","C")
        grafo.adicionaAresta("F","A")

        #resultados
        arrResultadoPorVertice = [
                                    {"A":2,"B":1,"C":3,"D":1,"E":1,"F":1},#indegree
                                    #{"A":0,"B":0,"C":0,"D":0,"E":0,"F":0},#coeficiente de clusterizacao distancia = 1
                                    #{"A":0,"B":0,"C":0,"D":0,"E":0,"F":0},#coeficiente de clusterizacao distancia = 2
                                    #{"A":0,"B":0,"C":0,"D":0,"E":0,"F":0},#coeficiente de clusterizacao distancia = 3
                                  ]
        #navega nas features
        vertices = grafo.getvertices()
        for i,feat in enumerate(arrFeaturesImplementadas):
            #para cada feature, calcula o resultado
            dictResultado = feat.compute_feature(grafo)
            #navega no resultado de cada vértice
            for posVertice,resultado in dictResultado.items():
                self.assertAlmostEqual(arrResultadoPorVertice[i][vertices[posVertice]], #resultado esperado da feature na posicao i, vertcie na posicao posGrafo
                                        resultado,#resultado obtido
                                        3,# numero de casas decimais que devem ser iguais nesse resultado
                                        "A feature "+feat.name+" produziu um resultado errado para o vértice "+vertices[posVertice]+". Resultado esperado: "+str(arrResultadoPorVertice[i][vertices[posVertice]])+" resulado obtido: "+str(resultado)
                                        )
            print(feat.name+" [OK]")

if __name__ == "__main__":
    unittest.main()
