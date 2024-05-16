import networkx as nx
import matplotlib.pyplot as plt
import env.network
import config.set_config
import config.network_config
import config.agents_config


def secgame():
    conf = config.set_config.Config(20, 40, True, True,
                                    True, True, True)
    conf.set_config_network()
    conf.set_config_red_agent()
    conf.set_config_blue_agent()
    network = env.network.Network()
    G = network.create_network_graph()
    nx.draw_spring(G, with_labels=True, node_color="Green")
    plt.show()
    matrix = network.matrix_graph()
    print(matrix)
    tensor = network.tensor_graph()
    print(tensor)


secgame()
