from env.agents.create_agent import Agent
from env.envNetwork import EnvNetwork
from env.network import Network
import config.set_config
import config.network_config
import config.agents_config
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


conf = config.set_config.Config(20, 40, False, True,
                                True, True, False, 5, True)
conf.set_config_network()
conf.set_config_red_agent()
conf.set_config_blue_agent()
red_rewards = [0, -5, -1, 1]
blue_rewards = [-1, -5, 10]
max_time = 20  # кол-во ходов
red_action_var = [1, 2, 3]
blue_action_var = [1, 2]
network = Network()
# g = network.create_network_graph()
g = network.networkGraph
nx.draw_spring(g, with_labels=True, node_color="Green")
plt.show()
env = EnvNetwork(red_rewards, blue_rewards, max_time, red_action_var, blue_action_var, network)
env.seed(15)
obs, info = env.reset()

print(env.env[1])

blue = Agent(("Blue", "Random"), ["test"]).create_agent()
blue.set_policy(env)
print(len(blue.policy))
print(f"Стандартная политика синего: {blue.policy}")

red = Agent(("Red", "Random"), ["test"]).create_agent()
red.set_policy(env)
print(f"Стандартная политика красного: {red.policy}")
#print(f"Политика при нахождениие красного в 14 узле {red.policy[14]}")
#print(f"Выбор действия красного: {red.get_action(env.red_state[0], env)}")

red_total_reward = 0
graph_red = nx.Graph()
for i in range(max_time):
    print(f"Пространство действий красного: {env.red_action_space}")
    action = red.get_action(env.red_state[0], env)
    state, rewards, terminated, info = env.step(action, "red")
    print(state[0], rewards, terminated, info)
    red_total_reward += rewards
    print(f"Состояние компрометации: \n {state[1][1]}")
    if action[0] != action[1]:
        graph_red.add_edge(action[0], action[1])
        print(graph_red)
        nx.draw_spring(graph_red, with_labels=True, node_color="Red")
        plt.show()
print(f"Путь красного: {env.red_trajectory}")
print(f"Награда красного: {red_total_reward}")
