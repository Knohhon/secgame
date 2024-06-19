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

elite_session_red = []
elite_session_blue = []

red_total_reward = 0
red_rewards_list = []
blue_total_reward = 0
blue_rewards_list = []
graph_red = nx.Graph()
old_red_rewards_list = []
old_blue_rewards_list = []
test_f = False

for grade in range(3):
    for generation in range(100):
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
                    nx.draw_spring(graph_red, with_labels=True, node_color="Red")
                    plt.show()

                # print(f"Путь красного: {env.red_trajectory}")
                print(f"Награда красного: {red_total_reward}")
                # red_all_trajectories.append([red_total_reward] + env.red_trajectory)
            else:
                print(f"Пространство действий синего: {env.blue_action_space}")
                action = blue.get_action(i - 1, env)
                print(f"Действие синего {len(action)}")
                state, rewards, terminated, info = env.step(action, "blue")
                print(f"Blue: {rewards, terminated, info}")
                blue_total_reward += rewards
                # print(f"Фиксация проверки: \n {state[1][2]}")
                # print(f"Фиксация выключения: \n {state[1][3]}")
                print(f"Награда синего: {blue_total_reward}")
                # blue_all_trajectories.append([blue_total_reward] + env.blue_trajectory)
            if terminated:
                print("End")
                env.reset()
                break

        red_rewards_list.append([generation, red_total_reward])
        blue_rewards_list.append([generation, blue_total_reward])
        red_total_reward = 0
        blue_total_reward = 0

        graph_red = nx.Graph()

        obs, info = env.reset()
        red_all_trajectories = env.red_trajectories
        blue_all_trajectories = env.blue_trajectories
        elite_session_red_num = env.get_quantile(quantile, red_rewards_list)
        elite_session_red_list = [red_all_trajectories[x[0]] for x in elite_session_red_num]
        elite_session_blue = env.get_quantile(quantile, blue_rewards_list)
        red.update_policy(env, elite_session_red_list)

        print(f"Траектории Red: {red_all_trajectories}")
        print(f"Кол-во траекторий красного {len(red_all_trajectories)}")
        print(f"Номера лучших траекторий красного {elite_session_red_num}")
        print(f"Лучшие траеткории красного {elite_session_red_list}")
        print(f"Кол-во траекторий синего {len(blue_all_trajectories)}")
        print(f"Номера лучших траетории синего {elite_session_blue}")
        print(f"Награды красного: {red_rewards_list}")
        print(f"Награды синего: {blue_rewards_list}")
    old_red_rewards_list += red_rewards_list
    old_blue_rewards_list += blue_rewards_list

    red_total_reward = 0
    red_rewards_list = []
    blue_total_reward = 0
    blue_rewards_list = []


red_total_reward = 0
red_rewards_list = []
blue_total_reward = 0
blue_rewards_list = []

for generation in range(100):
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
                nx.draw_spring(graph_red, with_labels=True, node_color="Red")
                plt.show()

            # print(f"Путь красного: {env.red_trajectory}")
            print(f"Награда красного: {red_total_reward}")
            # red_all_trajectories.append([red_total_reward] + env.red_trajectory)
        else:
            print(f"Пространство действий синего: {env.blue_action_space}")
            action = blue.get_action(i - 1, env)
            print(f"Действие синего {len(action)}")
            state, rewards, terminated, info = env.step(action, "blue")
            print(f"Blue: {rewards, terminated, info}")
            blue_total_reward += rewards
            # print(f"Фиксация проверки: \n {state[1][2]}")
            # print(f"Фиксация выключения: \n {state[1][3]}")
            print(f"Награда синего: {blue_total_reward}")
            # blue_all_trajectories.append([blue_total_reward] + env.blue_trajectory)
        if terminated:
            print("End")
            env.reset()
            break

    red_rewards_list.append([generation, red_total_reward])
    blue_rewards_list.append([generation, blue_total_reward])
    red_total_reward = 0
    blue_total_reward = 0

    graph_red = nx.Graph()

    obs, info = env.reset()
    red_all_trajectories = env.red_trajectories
    blue_all_trajectories = env.blue_trajectories
    elite_session_red_num = env.get_quantile(quantile, red_rewards_list)
    elite_session_red_list = [red_all_trajectories[x[0]] for x in elite_session_red_num]
    elite_session_blue = env.get_quantile(quantile, blue_rewards_list)
    red.update_policy(env, elite_session_red_list)

    print(f"Траектории Red: {red_all_trajectories}")
    print(f"Кол-во траекторий красного {len(red_all_trajectories)}")
    print(f"Номера лучших траекторий красного {elite_session_red_num}")
    print(f"Лучшие траеткории красного {elite_session_red_list}")
    print(f"Кол-во траекторий синего {len(blue_all_trajectories)}")
    print(f"Номера лучших траетории синего {elite_session_blue}")
    print(f"Награды красного: {red_rewards_list}")
    print(f"Награды синего: {blue_rewards_list}")
    print(f"Старые награды красного {old_red_rewards_list}")
    print(f"Старые награды синего {old_blue_rewards_list}")

old_red_r = [_[1] for _ in old_red_rewards_list]
red_r = [_[1] for _ in red_rewards_list]
old_blue_r = [_[1] for _ in old_blue_rewards_list]
blue_r = [_[1] for _ in blue_rewards_list]

plt.subplot(211)
plt.plot(old_red_r, color="red")
plt.plot(red_r, color="black")
plt.xlabel("Generation")
plt.ylabel("Total reward")

plt.subplot(212)
plt.plot(old_blue_r, color="blue")
plt.plot(blue_r, color="black")
plt.xlabel("Generation")
plt.ylabel("Total reward")

plt.show()
