from config import network_config
import networkx as nx
import random
import numpy as np


class Network:

    def __init__(self):
        self.count_layers = network_config.NetworkConfig.count_layers
        self.count_nodes = network_config.NetworkConfig.node_count
        self.count_edges = network_config.NetworkConfig.edge_count
        self.networkGraph = nx.Graph()

        # кол-во слоев в тензоре зависит от кол-ва возможных состояний узлов
        self.count_layers = network_config.NetworkConfig.count_layers
        self.list_of_nodes = []
        self.list_of_edges = []

    def check_config(self):
        if network_config.NetworkConfig.random_edges:
            print("Check Random edges")
            self.list_of_edges, self.list_of_nodes = self.create_random_edges(self.count_nodes, self.count_edges)

    @staticmethod
    def create_random_edges(count_nodes, count_edges):
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
        self.check_config()
        self.networkGraph.add_edges_from(self.list_of_edges)
        return self.networkGraph

    def matrix_graph(self):
        matrix_graph = nx.to_numpy_array(self.networkGraph)
        return matrix_graph

    def tensor_graph(self):
        matrix = self.matrix_graph()
        size = matrix.size
        for i in range(self.count_layers):
            matrix += np.zeros(matrix.shape)
        tensor = matrix.reshape(self.count_layers, size)
        return tensor





