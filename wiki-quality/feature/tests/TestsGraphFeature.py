from feature.featureImpl.graph import *
from feature.features import FeatureVisibilityEnum
from utils.basic_entities import FormatEnum,LanguageEnum,FeatureTimePerDocumentEnum
from feature.grafolistaadjacencia import grafolistaadjacencia
import unittest
class TestGraphFeatures(unittest.TestCase):
    def testFeatures(self):
        #o construtor possui os parametros pq são herdados de feature.features.FeatureCalculator (ver no arquivo feature/feature.py)
        #caso tenha mais elementos implementados (parametros) criar um novo construtor e chamar o super (ver classe Clusterizacao)
<<<<<<< HEAD
        arrFeaturesImplementadas = [#Indegree("Indegree","Indegree Metric metric","reference", FeatureVisibilityEnum.public,
                                     #       FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS),
                                #Outdegree("Outdegree","Outdegree Metric of vertex","reference", FeatureVisibilityEnum.public,
                                 #                                   FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS),
                                #AssortativeInputInput("Assortative Input Input", "Assortative Input/Input Metric", "reference",
                                 #           FeatureVisibilityEnum.public,FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS),
                                #AssortativeInputOutput("Assortative Input Output", "Assortative Input/Output Metric", "reference", FeatureVisibilityEnum.public,
                                 #           FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS),
                                #AssortativeOutputInput("Assortative Output Input", "Assortative Output/Input Metric", "reference", FeatureVisibilityEnum.public,
                                 #               FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS),
                                #AssortativeOutputOutput("Assortative Output Output", "Assortative Output/Output Metric", "reference", FeatureVisibilityEnum.public,
                                 #               FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS),
                                pageRank("pageRank", "pageRank Metric say how much popular is this article","reference", FeatureVisibilityEnum.public,
                                        FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS),
                                #Reciprocity("Reciprocity", "Reciprocity Metric of vertex", "reference", FeatureVisibilityEnum.public,
                                #            FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS),
=======
        arrFeaturesImplementadas = [Indegree("Indegree","Indegree Metric metric","reference", FeatureVisibilityEnum.public,
                                            FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS),
                                Outdegree("Outdegree","Outdegree Metric of vertex","reference", FeatureVisibilityEnum.public,
                                                                    FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS),
                                AssortativeInputInput("Assortative Input Input", "Assortative Input/Input Metric", "reference",
                                            FeatureVisibilityEnum.public,FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS),
                                AssortativeInputOutput("Assortative Input Output", "Assortative Input/Output Metric", "reference", FeatureVisibilityEnum.public,
                                            FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS),
                                AssortativeOutputInput("Assortative Output Input", "Assortative Output/Input Metric", "reference", FeatureVisibilityEnum.public,
                                                FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS),
                                AssortativeOutputOutput("Assortative Output Output", "Assortative Output/Output Metric", "reference", FeatureVisibilityEnum.public,
                                                FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS),
                                #pageRank("pageRank", "pageRank Metric say how much popular is this article","reference", FeatureVisibilityEnum.public,
                                #        FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS),
                                Reciprocity("Reciprocity", "Reciprocity Metric of vertex", "reference", FeatureVisibilityEnum.public,
                                            FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS),
>>>>>>> c085ecd25378475edc57587675a1fce8994dc996
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
     
     #   grafo.adicionaAresta("A","B")
      #  grafo.adicionaAresta("A","C")
       # grafo.adicionaAresta("A","F")
        #grafo.adicionaAresta("B","D")
     #   grafo.adicionaAresta("B","C")
      #  grafo.adicionaAresta("B","A")
       # grafo.adicionaAresta("C","E")
     #   grafo.adicionaAresta("E","C")
      #  grafo.adicionaAresta("F","A")
        grafo.adicionaAresta("A","D")
        grafo.adicionaAresta("B","A")
        grafo.adicionaAresta("B","C")
        grafo.adicionaAresta("D","B")
        grafo.adicionaAresta("D","A")
        #resultados
        arrResultadoPorVertice = [
<<<<<<< HEAD
                                    #{"A":2,"B":1,"C":3,"D":1,"E":1,"F":1},#indegree
                                    #{"A":3,"B":3,"C":1,"D":0,"E":1,"F":1}, #outdegree
                                    #{"A":1.2,"B":0.5,"C":3,"D":0,"E":0.333,"F":0.5}, #AssortativeInputInput
                                    #{"A":1.2,"B":0.75,"C":3,"D":0,"E":1,"F":0.333}, #AssortativeInputOutput
                                    #{"A":1.8,"B":1.5,"C":1,"D":0,"E":0.333,"F":0.5}, #AssortativeOutputInput
                                    #{"A":1.8,"B":2.25,"C":1,"D":0,"E":1,"F":0.333}, #AssortativeOutputOutput
                                    {"A":0.286544,"B":0.213456,"C":0.191658,"D":0.308342}, #pageRank
                                    #{"A":0.667,"B":0.333,"C":1,"D":0,"E":1,"F":1}, #reciprocity
=======
                                    {"A":2,"B":1,"C":3,"D":1,"E":1,"F":1},#indegree
                                    {"A":3,"B":3,"C":1,"D":0,"E":1,"F":1}, #outdegree
                                    {"A":1.2,"B":0.5,"C":3,"D":0,"E":0.333,"F":0.5}, #AssortativeInputInput
                                    {"A":1.2,"B":0.75,"C":3,"D":0,"E":1,"F":0.333}, #AssortativeInputOutput
                                    {"A":1.8,"B":1.5,"C":1,"D":0,"E":0.333,"F":0.5}, #AssortativeOutputInput
                                    {"A":1.8,"B":2.25,"C":1,"D":0,"E":1,"F":0.333}, #AssortativeOutputOutput
                                    #{"A":0.222,"B":0.056,"C":0.278,"D":0,"E":0.278,"F":0.056}, #pageRank
                                    {"A":0.667,"B":0.333,"C":1,"D":0,"E":1,"F":1}, #reciprocity
>>>>>>> c085ecd25378475edc57587675a1fce8994dc996
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
                                        "A feature "+feat.name+" produziu um resultado errado para o vértice "+vertices[posVertice]+". Resultado esperado: "+str(arrResultadoPorVertice[i][vertices[posVertice]])+" resultado obtido: "+str(resultado)
                                        )
            print(feat.name+" [OK]")

if __name__ == "__main__":
    unittest.main()
