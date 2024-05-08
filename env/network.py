from config import network_config

class Network(network_config):
    def __init__(self):

    def check_config(self):
        if network_config.NetworkConfig.random_edges == True:
