from config import network_config
import networkx as nx
import random
import numpy as np


class Network:
    def __init__(self):
        self.count_nodes = network_config.NetworkConfig.node_count
        self.count_edges = network_config.NetworkConfig.edge_count

    def check_config(self):
        if network_config.NetworkConfig.random_edges:
            self.create_random_edges(self.count_nodes, self.count_edges)

    @staticmethod
    def create_random_edges(count_nodes, count_edges):
        list_of_nodes = [x for x in range(count_nodes)]
        random.shuffle(list_of_nodes)
        list_of_edges = []
        for i in range(count_edges):
            edge = [list_of_nodes[i], list_of_nodes[i+1]]
            list_of_edges.append(edge)



