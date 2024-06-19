import random
from typing import Any, Tuple, Dict, Type

from gym.core import ActType
from gymnasium.core import ObsType
from gymnasium.utils import seeding

from env.network import Network
import numpy as np
import pygame as pg
import gymnasium as gym
from gymnasium import spaces


class EnvNetwork(gym.Env):

    def __init__(self, red_rewards: list, blue_rewards: list, max_time, red_action_var: list, blue_action_var: list,
                 network: Network):
        super().__init__()
        self.network = network
        self.env = None
        #self.metadata = {'render.modes': ['human', 'rgb_array'], 'video.frames_per_second': 10}
        # self.observation_space = spaces.Graph(node_space=self.network.list_of_nodes,
        #                                      edge_space=self.network.list_of_edges)
        """
        3 действия: 1 - остаться на месте, 2 - скомпрометировать соседний узел,
        3 - переместиться в другой, уже скомпрометированный узел
        """
        self.blue_trajectory = []
        self.blue_trajectories = []
        self.red_trajectory = []
        self.red_trajectories = []
        self.attacks = []  # Скомпрометированные ноды
        self.defenses = []  # Проверенные ноды
        self.off_node = []  # Выключеные ноды
        self.blue_state = []
        self.red_rewards = red_rewards
        self.blue_rewards = blue_rewards
        self.max_time = max_time
        self.current_time = 0
        self.terminated = False
        # self.render_on =  False
        self.red_action_var = red_action_var
        self.red_state = None  # текущее положение задается номером узла, номерами соседних узлов
        self.blue_action_var = blue_action_var
        self.red_action_space = []
        """
        0 - проверка определенного узла; 1 - выключение определенного узла;
        """
        self.blue_action_space = []

        self.seed()
        self.info_type = {"red": ["Ход red прошел успешно", "Проблема с ходом red"],
                          "blue": ["Ход blue прошел успешно", "Проблема с ходом blue"],
                          "env": ["Ошибка", "Начало хода", "Выбран неправильный тип агента",
                                  "Выбрано действие, которого нет в списке",
                                  "Красный проиграл, потому что синий выключил текущий узел красного"]}
        self.info = ""

    """
    первые 3 - награды за дейтсвия красного, 4 - награда за шаг, в котором красный не был найден
    red_rewards = [0, -5, -1, 1]
    первые 2 - награды за действия синего, 3 - награда за выключенный скомпрометированный узел
    blue_rewards = [-1, -5, 10]
    wib_reward = 100 <- награда за победу, для красного и синего одинакова
    """

    def step(self, action, agent_type):
        """
        :param action:

        [1 - остаться на месте,
        2 - скомпрометировать соседний узел (агент перемещается в этот узел) (узел указать),
        3 - переместиться в другой скомпрометированный узел (узел указать)] - red;
        [1 - проверка определенного узла (узел указать), 2 - выключение определенного узла (узел указать)] - blue
        :return:
        """
        self.info = ""
        print(f"Действие: {action}")
        red_reward = -1000
        blue_reward = -1000
        reward = 0
        self.info += self.info_type["env"][1]
        if agent_type == "red":
            current_red_action_space = self.red_action_space
            if action[0] in self.off_node:
                self.info += self.info_type["env"][4]
                self.terminated = True
            if action[2] not in self.red_action_var:
                self.info += self.info_type["env"][3]
                return red_reward, blue_reward, False, self.info
            red_step = action
            if red_step[2] == 1:
                red_reward = self.red_rewards[0]
            elif red_step[2] == 2:
                self.red_state = [red_step[1]] + self.set_red_neighbours_nodes(red_step[1])
                self.red_action_space = self.set_red_action_space(self.red_state)
                red_reward = self.red_rewards[1]
                num_node = red_step[1]
                self.set_red_env_state(num_node, num_layers=1)
                self.attacks.append(red_step[1])
            elif red_step[2] == 3:
                self.red_state = [red_step[1]] + self.set_red_neighbours_nodes(red_step[1])
                self.red_action_space = self.set_red_action_space(self.red_state)
                red_reward = self.red_rewards[2]
            if red_reward not in self.red_rewards:
                self.info += ' ' + self.info_type["red"][1]
                print(red_reward, self.red_rewards, self.info)
            else:
                pass
            red_reward += self.red_rewards[3]
            reward = red_reward
            self.red_trajectory.append([reward, action[0], action, current_red_action_space])
            print(f"Траектория красного: {self.red_trajectory}")

        elif agent_type == "blue":
            self.blue_trajectory.append([action, self.blue_state])
            blue_step = action
            num_node = blue_step[0]
            if blue_step[1] == 1:
                self.set_blue_state(num_node, num_layers=2)
                blue_reward = self.blue_rewards[0]
            elif blue_step[1] == 2:
                self.set_blue_state(num_node, num_layers=3)
                self.off_node.append(blue_step[0])
                blue_reward = self.blue_rewards[1]
            if blue_reward not in self.blue_rewards:
                self.info += self.info_type["blue"][1]
            else:
                pass
            reward = blue_reward
        else:
            self.info += self.info_type["env"][2]
        print(f"Текущий ход: {self.current_time}")
        if self.current_time + 1 == self.max_time:
            self.terminated = True
            print(f"Конец ходов {self.terminated}")
        self.current_time += 1
        state = [self.red_state, self.blue_state]
        observation = state
        # observation; reward; terminated - если достиг финального состояния; truncated - таймлимит; info;
        return state, reward, self.terminated, self.info

    def reset(self, seed=None, options=None) -> tuple[Any, Type[dict[Any, Any]]]:
        """
        Перезапуск среды, установка значений к стартовым значениям
        :return:
        """
        self.env = self.network.tensor
        self.red_state = [self.seed()]
        self.red_state += self.set_red_neighbours_nodes(self.red_state[0])
        self.blue_state = self.env
        self.red_action_space = self.set_red_action_space()
        self.blue_action_space = self.set_blue_action_space()
        self.set_red_env_state(self.red_state[0], num_layers=1)
        self.attacks = []
        self.attacks.append(self.red_state[0])
        self.current_time = 0
        if self.terminated:
            self.red_trajectories.append(self.red_trajectory)
            self.blue_trajectories.append(self.blue_trajectory)
            self.terminated = False
            self.info = ""
        obs = tuple[self.red_state, self.blue_state]
        info = dict['Reset', 1]
        self.red_trajectory = []
        self.blue_trajectory = []
        return obs, info

    def seed(self, seed=None):
        if seed is not None:
            seed = np.random.randint(seed)
        else:
            seed = np.random.randint(len(self.network.list_of_nodes))
        return seed

    def render(self, mode='human'):
        pass

    def close(self):
        """
        Очищает все значения переменных
        :return:
        """
        self.env = np.nan
        self.red_action_var = np.nan
        self.red_action_space = np.nan
        self.blue_action_var = np.nan
        self.blue_action_space = np.nan
        self.blue_trajectory = []
        self.blue_trajectories = []
        self.red_trajectory = []
        self.red_trajectories = []
        self.attacks = []
        self.defenses = []
        self.red_state = [0]
        self.blue_state = np.nan
        self.red_rewards = np.nan
        self.blue_rewards = np.nan
        self.max_time = np.nan
        self.current_time = np.nan
        self.terminated = False

    def set_red_action_space(self, red_state: list = None) -> list:
        """
        [текущее состояние агента (местоположение),
         состояние агента после действия (метопололжение), действие, которое может совершить red, ]
        :return:
        """
        if red_state is None:
            red_state = self.red_state
        if hasattr(EnvNetwork, "red_state"):
            print(red_state)
        list_edges = self.network.list_of_edges
        red_space_array = []
        for i in range(len(red_state)):
            pairs = [-1, -1, -1]
            for action in self.red_action_var:
                if action == 1:
                    pairs = [red_state[0], red_state[0], action]
                elif action == 3 and red_state[i] in self.attacks:
                    pairs = [red_state[0], red_state[i], action]
                elif action == 2 and red_state[i] not in self.attacks and red_state[i] != red_state[0]:
                    pairs = [red_state[0], red_state[i], action]
            #print("Возможное дейсвтие Red:  " + str(pairs))
            red_space_array += [pairs]
        #print("Пространство возможных действий Red: " + str(red_space_array))
        assert (len(red_space_array) != 0)
        red_space_array = self.update_red_actions_array(red_space_array)
        return red_space_array

    def set_blue_action_space(self):
        """
        [узел - цель действия, дейсвие blue]
        :return:
        """
        blue_space_array = []
        list_nodes = self.network.list_of_nodes
        for node in list_nodes:
            for action in self.blue_action_var:
                pairs = [node, action]
                blue_space_array += [pairs]
                # print("Возможное действие Blue: ", pairs)
        assert (len(blue_space_array) != 0)
        return blue_space_array

    def set_red_neighbours_nodes(self, red_state):
        """
        Формирует список узлов-соседей текущего положения red
        :param red_state:
        :return:
        """
        red_neighbours = []
        #print("Список узлов: ", self.network.list_of_nodes)
        #print("Список ребер: ", self.network.list_of_edges)
        # print("Среда: ", self.env)
        for i in range(len(self.network.list_of_nodes)):
            node = self.env[0][red_state][i]
            if node == 1:
                #print("Состояние красного: ", red_state)
                #print("Узел: ", node, self.env[0], red_state, i)
                red_neighbours.append(i)
        return red_neighbours

    def set_red_env_state(self, num_node, num_layers):
        """
        Заполняет слои характеристик узлов в тензоре единицами
        :param num_node:
        :param num_layers:
        :return:
        """
        print(f'')
        self.env[num_layers][num_node][num_node] = 1

    def set_blue_state(self, num_node, num_layers):
        """
        Заполняет слои известных характеристик узлов в тензоре единицами
        :param num_node:
        :param num_layers:
        :return:
        """
        self.blue_state[num_layers][num_node][num_node] = 1

    def sort_trajectories(self, trajectories: list):
        if len(trajectories) <= 1:
            return trajectories
        else:
            border = trajectories[0]
            left = [x for x in trajectories[1:] if x[1] >= border[1]]
            right = [x for x in trajectories[1:] if x[1] < border[1]]
            return self.sort_trajectories(left) + [border] + self.sort_trajectories(right)

    def get_quantile(self, quantile, trajectories):
        sorted_list = self.sort_trajectories(trajectories)
        q = int(len(sorted_list) * quantile)
        elite = [0] * q
        if q > 0:
            for i in range(q):
                elite[i] = sorted_list[i]
        return elite

    def set_elite_session(self, quantile, trajectories):
        id_reward_elite = self.get_quantile(quantile, trajectories)
        for elite in id_reward_elite:
            return self.blue_trajectories[elite[0]]

    def update_red_actions_array(self, action_space):
        current_action_space = action_space
        for action in range(len(action_space)):
            if action >= len(action_space):
                break
            elif current_action_space[action][1] in self.off_node:
                # print(f"removed {current_action_space[action]}")
                current_action_space.remove(current_action_space[action])
            elif current_action_space[action][2] == 2 and current_action_space[action][2] in self.attacks:
                # print(f"removed {current_action_space[action]}")
                current_action_space.remove(current_action_space[action])
            elif current_action_space[action][2] == 3 and current_action_space[action][2] not in self.attacks:
                # print(f"removed {current_action_space[action]}")
                action_space.remove(action_space[action])
        return current_action_space

