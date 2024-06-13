from env.agents.create_agent import Agent
from env.envNetwork import EnvNetwork
from env.network import Network
import config.set_config
import config.network_config
import config.agents_config
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


conf = config.set_config.Config(5, 10, False, True,
                                True, True, False, 5, True)
conf.set_config_network()
conf.set_config_red_agent()
conf.set_config_blue_agent()
red_rewards = [0, -5, -1, 1]
blue_rewards = [-1, -5, 10]
quantile = 0.1
max_time = 20 * 2 # кол-во ходов * 2, т к агенты ходят по очереди
red_action_var = [1, 2, 3]
blue_action_var = [1, 2]
network = Network()
# g = network.create_network_graph()
g = network.networkGraph
nx.draw_spring(g, with_labels=True, node_color="Green")
plt.show()
env = EnvNetwork(red_rewards, blue_rewards, max_time, red_action_var, blue_action_var, network)
env.seed()
obs, info = env.reset()

blue = Agent(("Blue", "Random"), ["test"]).create_agent()
blue.set_policy(env)
print(len(blue.policy))
print(f"Стандартная политика синего: {blue.policy}")

red = Agent(("Red", "Random"), ["test"]).create_agent()
red.set_policy(env)
print(f"Стандартная политика красного: {red.policy}")
#print(f"Политика при нахождениие красного в 14 узле {red.policy[14]}")
#print(f"Выбор действия красного: {red.get_action(env.red_state[0], env)}")

red_all_trajectories = []

blue_all_trajectories = []

red_total_reward = 0
red_rewards_list = []
blue_total_reward = 0
blue_rewards_list = []
graph_red = nx.Graph()
test_f = False

for generation in range(10):
    for i in range(env.max_time):
        if i % 2 == 0:
            # print(f"Пространство действий красного: {env.red_action_space}")
            action = red.get_action(env.red_state[0], env)
            state, rewards, terminated, info = env.step(action, "red")
            print(f"Red: {rewards, terminated, info}")
            red_total_reward += rewards
            # print(f"Состояние компрометации: \n {state[1][1]}")
            if action[0] != action[1] and test_f:
                graph_red.add_edge(action[0], action[1])
                print(graph_red)
                nx.draw_spring(graph_red, with_labels=True, node_color="Red")
                plt.show()

            # print(f"Путь красного: {env.red_trajectory}")
            print(f"Награда красного: {red_total_reward}")
            # red_all_trajectories.append([red_total_reward] + env.red_trajectory)
        else:
            # print(f"Пространство действий синего: {env.blue_action_space}")
            action = blue.get_action(i - 1, env)
            state, rewards, terminated, info = env.step(action, "blue")
            print(f"Blue: {rewards, terminated, info}")
            blue_total_reward += rewards
            # print(f"Фиксация проверки: \n {state[1][2]}")
            # print(f"Фиксация выключения: \n {state[1][3]}")
            print(f"Награда синего: {blue_total_reward}")
            # blue_all_trajectories.append([blue_total_reward] + env.blue_trajectory)
    red_rewards_list.append(red_total_reward)
    blue_rewards_list.append(blue_total_reward)
    red_total_reward = 0
    blue_total_reward = 0

    obs, info = env.reset()
    red_all_trajectories = env.red_trajectories
    blue_all_trajectories = env.blue_trajectories
    print(f"Траектории Red: {red_all_trajectories}")
    print(f"Награды красного: {red_rewards_list}")
    print(f"Награды синего: {blue_rewards_list}")

