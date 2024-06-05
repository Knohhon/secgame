from config import network_config
import networkx as nx
import random
import numpy as np


class Network:

    def __init__(self):
        self.count_layers = network_config.NetworkConfig.count_layers
        self.count_nodes = network_config.NetworkConfig.node_count
        self.count_edges = network_config.NetworkConfig.edge_count

        # кол-во слоев в тензоре зависит от кол-ва возможных состояний узлов
        self.count_layers = network_config.NetworkConfig.count_layers
        self.list_of_nodes = []
        self.list_of_edges = []

        self.networkGraph = nx.Graph()
        self.tensor = self.tensor_graph()

    def check_config(self):
        if network_config.NetworkConfig.random_edges:
            print("Random Edges: ", network_config.NetworkConfig.random_edges)
            print("Check Random edges")
            self.list_of_edges, self.list_of_nodes = self.create_random_edges(self.count_nodes, self.count_edges)
            assert len(self.list_of_edges) != 0 and len(self.list_of_nodes) != 0
        elif network_config.NetworkConfig.test:
            print("Check Test network")
            self.list_of_edges, self.list_of_nodes = self.get_test_graph()

    @staticmethod
    def create_random_edges(self, count_nodes, count_edges):
        print("Creating random edges...")
        print("Count nodes: ", count_nodes)
        _ = int(count_nodes)
        print(_)
        list_of_nodes = [x for x in range(_)]
        random.shuffle(list_of_nodes)
        list_of_edges = []
        for _ in range(int(count_edges)):
            edge = random.sample(list_of_nodes, 2)
            list_of_edges.append(edge)
        print(list_of_edges)
        return list_of_edges, list_of_nodes

    def create_network_graph(self) -> nx.Graph:
        print("Creating Network Graph...")
        print("List of edges: ", self.list_of_edges)
        self.check_config()
        self.networkGraph.add_edges_from(self.list_of_edges)
        return self.networkGraph

    def matrix_graph(self):
        self.create_network_graph()
        matrix_graph = np.zeros((len(self.list_of_nodes), len(self.list_of_nodes)))
        # print("Matrix Graph ", matrix_graph)
        for i, j in self.list_of_edges:
            # print(">>>> ", i, j, type(i), type(j), " <<<<")
            matrix_graph[i][j] = 1.0
            matrix_graph[j][i] = 1.0
        return matrix_graph

    def tensor_graph(self):
        matrix = self.matrix_graph()
        list_of_matrix = [matrix]
        # print("Матрица смежности: ", list_of_matrix)
        for i in range(self.count_layers):
            zeros_matrix = np.zeros_like(matrix)
            # print("Пустая матрица: " + str(zeros_matrix))
            list_of_matrix.append(zeros_matrix)
        # print("Все матрицы: ", list_of_matrix)
        return list_of_matrix

    @staticmethod
    def get_test_graph():
        edges = [[5, 14], [10, 0], [10, 12], [2, 0], [6, 10], [11, 2], [5, 8], [3, 14],
                 [16, 8], [15, 11], [13, 2], [11, 10], [2, 16], [4, 1], [6, 1], [9, 4],
                 [18, 0], [18, 16], [6, 12], [19, 1], [2, 3], [7, 13], [13, 15], [19, 14],
                 [15, 17], [14, 9], [14, 18], [3, 6], [16, 3], [10, 9], [11, 3], [18, 12],
                 [4, 6], [9, 18], [4, 12], [11, 19], [17, 4], [8, 2], [12, 19], [17, 10]]
        print("Creating random edges...")
        print("Count nodes: ", 20)
        list_of_nodes = [x for x in range(20)]
        list_of_edges = edges
        return list_of_edges, list_of_nodes

