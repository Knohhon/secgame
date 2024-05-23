from env.envNetwork import EnvNetwork
from env.network import Network
import config.set_config
import config.network_config
import config.agents_config
import numpy as np

conf = config.set_config.Config(20, 40, True, True,
                                True, True, True, 4)
conf.set_config_network()
conf.set_config_red_agent()
conf.set_config_blue_agent()
red_rewards = [-1, 0, -5, 1]
blue_rewards = [-1, -5, 10]
max_time = 20  # кол-во ходов
red_action_var = [0, 1, 2]
blue_action_var = [0, 1]
start_red_state = [np.random.randint(20)]
network = Network()
G = network.create_network_graph()
env = EnvNetwork(red_rewards, blue_rewards, max_time, red_action_var, blue_action_var, network, start_red_state)
env.reset()
print(env.red_action_space)

print(env.blue_action_space)

