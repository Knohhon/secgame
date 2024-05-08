import network_config
import agents_config


class Config:

    def __init__(self, node_count, edge_count, random_edges, replace_to_node, compromise, close_node, repare):
        self.node_count = node_count
        self.edge_count = edge_count
        self.random_edges = random_edges
        self.replace_to_node = replace_to_node
        self.compromise = compromise
        self.close_node = close_node
        self.repare = repare

    def set_config_network(self, node_count, edge_count, random_edges):
        network_config.NetworkConfig.node_count = self.node_count
        network_config.NetworkConfig.edge_count = self.edge_count
        network_config.NetworkConfig.random_edges = self.random_edges

    def set_config_red_agent(self, replace_to_node, compromise):
        agents_config.RedAgentConfig.red_replace_to_node = self.replace_to_node
        agents_config.RedAgentConfig.red_compromise = self.compromise

    def set_config_blue_agent(self, close_node, repare):
        agents_config.BlueAgentConfig.blue_close_node = self.close_node
        agents_config.BlueAgentConfig.blue_repare = self.repare








