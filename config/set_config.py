import network_config
import agents_config

class Config(network_config.NetworkConfig, agents_config.AgentsConfig):

#    def __init__(self):


    def set_config(node_count, edge_count, random_edges, replace_to_node, compromise, close_node, repare):
        set_config_network(node_count, edge_count, random_edges)
        set_config_red_agent(replace_to_node, compromise)
        set_config_blue_agent(close_node, repare)

