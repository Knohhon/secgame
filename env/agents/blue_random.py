import numpy as np

from env.agents.agent_interface import AgentInterface
from env.envNetwork import EnvNetwork


class BlueRandomAgent(AgentInterface):
    def __init__(self):
        super().__init__()
        self.policy = None

    def get_action(self, num_step, env: EnvNetwork = None) -> list[int, int]:
        prob = self.policy[num_step]
        action = np.random.choice(len(env.blue_action_space), p=prob)
        return env.blue_action_space[action]

    def update_policy(self, elite_session: list, env: EnvNetwork = None):
        """
        Updates the policy based on the elite session
        :param elite_session: list
        :param env: EnvNetwork
        """
        new_policy = np.zeros(self.len_state(env), env.blue_action_space)

        for session in elite_session:
            for state, action in (session['state'], session['action']):
                s = self.interpretate_state(env, state, action[2])
                a = self.search_action(env, action)
                new_policy[s][a] = 1

        for state in range(env.blue_action_space):
            if sum(new_policy[state]) == 0:
                new_policy[state] = [1/len(env.blue_action_space) for x in range(len(env.blue_action_space))]
            elif sum(new_policy[state]) > 1:
                new_policy[state] /= sum(new_policy[state])

        self.policy = new_policy


    @staticmethod
    def len_state(env: EnvNetwork = None) -> int:
        s = 0
        for i in range(len(env.network.list_of_nodes)):
            for j in range(len(env.blue_action_var) + 1):
                s += 1
        return s

    @staticmethod
    def interpretate_state(env: EnvNetwork, state: int, action: int) -> int:
        """
        Возвращает номер строки в мартрице policy
        :param env: EnvNetwork
        :param state: int
        :param action: int
        :return: s: int
        """
        s = 0
        for i in range(len(env.network.list_of_nodes)):
            for j in range(len(env.blue_action_var) + 1):
                s += 1
                if i == state and j == action:
                    return s
        print(f"Номер состояния для {state, action} не найден")
        return -1

    @staticmethod
    def search_action(env: EnvNetwork, action: list) -> int:
        """
        Возвращает номер действия синего агента в строке матрицы policy
        :param env: EnvNetwork
        :param action: list
        :return: a: int
        """
        a = 0
        for i in range(len(env.blue_action_space)):
            a = 0
            if env.blue_action_space[i] is action:
                return a
        print(f"Номер действия для {action} не найден")
        return -1

    def set_policy(self, env: EnvNetwork = None):
        print(env.network.list_of_nodes)
        print(self.len_state(env))
        self.policy = [0] * self.len_state(env)
        for i in range(self.len_state(env)):
            self.policy[i] = [1/len(env.blue_action_space) for x in range(len(env.blue_action_space))]



