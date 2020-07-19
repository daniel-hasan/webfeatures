from feature.featureImpl.graph import *
from feature.features import FeatureVisibilityEnum
from utils.basic_entities import FormatEnum,LanguageEnum,FeatureTimePerDocumentEnum
from feature.grafolistaadjacencia import grafolistaadjacencia
import unittest
class TestGraphFeatures(unittest.TestCase):
    def testFeatures(self):
        
        #cria o grafo:
        grafo = grafolistaadjacencia()

        grafo.adicionaAresta("A","B")
        grafo.adicionaAresta("A","C")
        grafo.adicionaAresta("A","F")
        grafo.adicionaAresta("B","D")
        grafo.adicionaAresta("B","C")
        grafo.adicionaAresta("B","A")
        grafo.adicionaAresta("C","E")
        grafo.adicionaAresta("E","C")
        grafo.adicionaAresta("F","A")
        
        
        #o construtor possui os parametros pq são herdados de feature.features.FeatureCalculator (ver no arquivo feature/feature.py)
        #caso tenha mais elementos implementados (parametros) criar um novo construtor e chamar o super (ver classe Clusterizacao)
        arrFeaturesImplementadas = [Indegree("Indegree","Indegree Metric metric","reference", FeatureVisibilityEnum.public,
                                            FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS),
                                    
                                Outdegree("Outdegree","Outdegree Metric of vertex","reference", FeatureVisibilityEnum.public,
                                                                    FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS),
                                    
                                AssortativeInputInput("Assortative Input Input", "Assortative Input/Input Metric", "reference",
                                            FeatureVisibilityEnum.public,FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS),
                                    
                                AssortativeInputOutput("Assortative Input Output", "Assortative Input/Output Metric", "reference", FeatureVisibilityEnum.public, FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS),
                                    
                                AssortativeOutputInput("Assortative Output Input", "Assortative Output/Input Metric", "reference", FeatureVisibilityEnum.public, FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS),
                                    
                                AssortativeOutputOutput("Assortative Output Output", "Assortative Output/Output Metric", "reference", FeatureVisibilityEnum.public, FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS),
                                    
                                PageRank("PageRank", "PageRank Metric say how much popular is this article","reference", FeatureVisibilityEnum.public, FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS,0.95,0.01),
                                    
                                Reciprocity("Reciprocity", "Reciprocity Metric of vertex", "reference", FeatureVisibilityEnum.public,
                                            FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS),
                                    
                                ClusteringCoefficient("Clustering Coefficient","Clustering Coefficient is a measure of the degree to which nodes in a graph tend to cluster together.","reference", FeatureVisibilityEnum.public, FormatEnum.HTML, FeatureTimePerDocumentEnum.MILLISECONDS, 1.0) ]
        

        #resultados
        arrResultadoPorVertice = [  {"A":2,"B":1,"C":3,"D":1,"E":1,"F":1},#indegree
                                    {"A":3,"B":3,"C":1,"D":0,"E":1,"F":1}, #outdegree
                                    {"A":1.2,"B":0.5,"C":3,"D":0,"E":0.333,"F":0.5}, #AssortativeInputInput
                                    {"A":1.2,"B":0.75,"C":3,"D":0,"E":1,"F":0.333}, #AssortativeInputOutput
                                    {"A":1.8,"B":1.5,"C":1,"D":0,"E":0.333,"F":0.5}, #AssortativeOutputInput
                                    {"A":1.8,"B":2.25,"C":1,"D":0,"E":1,"F":0.333}, #AssortativeOutputOutput
                                    {"A":0.05,"B":0.1,"C":0.05, "D":0.1,"E":0.05,"F":0.1}, #PageRank Larisse
                                    {"A":0.667,"B":0.333,"C":1,"D":0,"E":1,"F":1}, #reciprocity
                                    {"A":0.333,"B":0.333,"C":0.0,"D":0.0,"E":0.0,"F":0.0},#coeficiente de clusterizacao distancia = 1
                                    #{"A":0.0,"B":0.0,"C":0.0,"D":0.0,"E":0.0,"F":0.5},#coeficiente de clusterizacao distancia = 2
                                    #{"A":0.0,"B":0.0,"C":0.0,"D":0.0,"E":0.0,"F":0.0},#coeficiente de clusterizacao distancia = 3
                                  ]
        
        vertices = grafo.getvertices()
        #navega nas features
        for i,feat in enumerate(arrFeaturesImplementadas):
            
            #para cada feature, calcula o resultado
            dictResultado = feat.compute_feature(grafo)
            
            #navega no resultado de cada vértice
            for posVertice,resultado in dictResultado.items():
                
                self.assertAlmostEqual(arrResultadoPorVertice[i][vertices[posVertice]],resultado, 1, "A feature "+feat.name+" produziu um resultado errado para o vértice "+vertices[posVertice]+". Resultado obtido: "+str(arrResultadoPorVertice[i][vertices[posVertice]])+" resultado esperado: "+str(resultado))
                
            print(feat.name+" [OK]")

if __name__ == "__main__":
    unittest.main()
