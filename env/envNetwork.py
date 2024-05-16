from gymnasium.utils import seeding

from network import Network
import numpy as np
import pygame as pg
import gymnasium as gym
from gymnasium import spaces


class EnvNetwork(gym.Env):

    def __init__(self, red_rewards: list, blue_rewards: list, max_time, red_action_var: list, blue_action_var: list):
        super().__init__()
        self.network = Network()
        self.env = self.network.tensor_graph()
        self.metadata = {'render.modes': ['human', 'rgb_array'], 'video.frames_per_second': 10}
        self.observation_space = spaces.Graph(node_space=self.network.list_of_nodes,
                                              edge_space=self.network.list_of_edges)
        """
        3 действия: 0 - переместиться в другой, уже скомпрометированный, узел, 1 - остаться на месте,
        2 - скомпрометировать соседний узел
        """
        self.red_action_var = red_action_var
        self.red_action_space = self.set_red_action_space()
        """
        0 - проверка определенного узла; 1 - выключение определенного узла;
        """
        self.blue_action_var = blue_action_var
        self.blue_action_space = self.set_blue_action_space()
        self.blue_trajectory = []
        self.blue_trajectories = []
        self.red_trajectory = []
        self.red_trajectories = []
        self.attacks = []  # Скомпрометированные ноды
        self.defenses = []  # Проверенные ноды
        self.red_state = [0]  # текущее положение задается номером узла, номерами соседних узлов
        self.blue_state = self.env
        self.red_rewards = red_rewards
        self.blue_rewards = blue_rewards
        self.max_time = max_time
        self.current_time = 0
        self.terminated = False
        self.seed = self.seed()
        self.reset()
        self.message_type = {"red": ["Ход red прошел успешно", "Проблема с ходом red"],
                             "blue": ["Ход blue прошел успешно", "Проблема с ходом blue"],
                             "env": ["Ошибка", "Начало хода", "Выбран неправильный тип агента",
                                     "Выбрано действие, которого нет в списке"]}
        self.message = ""

    """
    первые 3 - награды за дейтсвия красного, 4 - награда за шаг, в котором красный не был найден
    red_rewards = [-1, 0, -5, 1]
    первые 2 - награды за действия синего, 3 - награда за выключенный скомпрометированный узел
    blue_rewards = [-1, -5, 10]
    wib_reward = 100 <- награда за победу, для красного и синего одинакова
    """

    def step(self, action, agent_type):
        """
        :param action:

        [0 - переместиться в другой скомпрометированный узел (узел указать), 1 - остаться на месте,
        2 - скомпрометировать соседний узел (агент перемещается в этот узел) (узел указать)] - red;
        [0 - проверка определенного узла (узел указать), 1 - выключение определенного узла (узел указать)] - blue
        :return:
        """
        red_reward = -1000
        blue_reward = -1000
        self.message += self.message_type["env"][1]
        if action not in self.red_action_var:
            self.message = self.message_type["env"][3]
            return red_reward, blue_reward, False, self.message
        if agent_type == "red":
            self.red_trajectory.append(self.red_state)
            red_reward = self.red_rewards[action[1]]
            red_step = self.red_action_space[action]
            if red_step[2] == 0:
                self.red_state = red_step[1] + self.set_red_neighbours_nodes(red_step[1])
                red_reward = self.red_rewards[0]
            elif red_step[2] == 1:
                red_reward = self.red_rewards[1]
            elif red_step[2] == 2:
                self.red_state = red_step[1] + self.set_red_neighbours_nodes(red_step[1])
                red_reward = self.red_rewards[2]
                self.attacks.append(red_step[1])
            if red_reward not in self.red_rewards:
                self.message += self.message_type["red"][1]
            else:
                pass

        elif agent_type == "blue":
            self.blue_trajectory.append(self.blue_state)
            blue_reward = self.blue_rewards[action]
            if blue_reward not in self.blue_rewards:
                self.message += self.message_type["blue"][1]
            else:
                pass
        else:
            self.message += self.message_type["env"][2]
        rewards = [red_reward, blue_reward]
        if self.current_time == self.max_time:
            self.terminated = True
        state = [self.red_state, self.blue_state]
        rewards = [red_reward, blue_reward]
        return state, rewards, self.terminated, self.message

    def reset(self):
        """
        Перезапуск среды, установка значений к стартовым значениям
        :return:
        """
        self.red_state = [self.seed[np.random.randint(len(self.seed))]]
        self.red_state += self.set_red_neighbours_nodes(self.red_state[0])
        self.blue_state = self.env
        if self.terminated:
            self.red_trajectories.append(self.red_trajectory)
            self.blue_trajectories.append(self.blue_trajectory)
            self.terminated = False
            self.message = ""

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def render(self, mode='human'):
        pass

    def close(self):
        pass

    def set_red_action_space(self):
        """
        [текущее состояние агента (местоположение),
         состояние агента после действия (метопололжение), действие, которое может совершить red, ]
        :return:
        """
        list_edges = self.network.list_of_edges
        red_space_array = np.array([])
        for i in range(len(self.red_state)):
            pairs = [-1, -1, -1]
            for action in self.red_action_var:
                if action == 1:
                    pairs = [self.red_state[0], self.red_state[0], action]
                elif action == 0 and self.red_state[i] in self.attacks:
                    pairs = [self.red_state[0], self.red_state[i], action]
                elif action == 2 and self.red_state[i] not in self.attacks:
                    pairs = [self.red_state[0], self.red_state[i], action]
            np.append(red_space_array, pairs)
        assert (len(red_space_array) != 0)
        return spaces.MultiDiscrete(red_space_array)

    def set_blue_action_space(self):
        """
        [узел - цель действия, дейсвие blue]
        :return:
        """
        blue_space_array = np.array([])
        list_nodes = self.network.list_of_nodes
        for node in list_nodes:
            for action in self.blue_action_var:
                pairs = [node, action]
                np.append(blue_space_array, pairs)
        assert (len(blue_space_array) != 0)
        return spaces.MultiDiscrete(blue_space_array)

    def set_red_neighbours_nodes(self, red_state):
        """
        Формирует список узлов-соседей текущего положения red
        :param red_state:
        :return:
        """
        red_neighbours = []
        for i in range(self.env.number_of_nodes):
            node = self.env[0][red_state][i]
            if node == 1:
                red_neighbours.append(i)
        return red_neighbours
