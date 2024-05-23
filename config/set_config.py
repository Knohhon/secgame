from config.network_config import NetworkConfig
from config.agents_config import RedAgentConfig, BlueAgentConfig


class Config:

    def __init__(self, node_count, edge_count, random_edges, replace_to_node, compromise,
                 close_node, repare, count_layers):
        self.node_count = node_count
        self.edge_count = edge_count
        self.random_edges = random_edges
        self.replace_to_node = replace_to_node
        self.compromise = compromise
        self.close_node = close_node
        self.repare = repare
        self.count_layers = count_layers

    def set_config_network(self):
        NetworkConfig.node_count = self.node_count
        NetworkConfig.edge_count = self.edge_count
        NetworkConfig.random_edges = self.random_edges
        NetworkConfig.count_layers = self.count_layers

    def set_config_red_agent(self):
        RedAgentConfig.red_replace_to_node = self.replace_to_node
        RedAgentConfig.red_compromise = self.compromise

    def set_config_blue_agent(self):
        BlueAgentConfig.blue_close_node = self.close_node
        BlueAgentConfig.blue_repare = self.repare










