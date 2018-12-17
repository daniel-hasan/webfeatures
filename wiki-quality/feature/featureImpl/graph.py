from feature import GraphBasedFeature
class Indegree(GraphBasedFeature):
        def compute_feature(self,graph):
                dic_result = {}
                for vertice_id in graph.get_vertice_ids():
                        dic_result[vertice_id] = len(graph.get_vertices_entrada(vertice_id))
                return dic_result
