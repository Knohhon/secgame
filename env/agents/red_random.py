import numpy as np

from env.agents.agent_interface import AgentInterface
from env.envNetwork import EnvNetwork


class RedRandomAgent(AgentInterface):
    def __init__(self, ):
        super().__init__()
        self.policy = None

    def get_action(self, state, env: EnvNetwork = None) -> list[int, int, int]:
        prob, current_action_space = self.update_current_action(env, state)
        print(f"Policy update by blue actions {prob, self.policy[state]}")
        print(prob, current_action_space)
        action = np.random.choice(len(current_action_space), p=prob)
        return current_action_space[action]

    def update_current_action(self, env: EnvNetwork = None, state: int = None):
        policy = self.policy[state]
        action_space = env.red_action_space
        if len(policy) != len(action_space):
            policy = [1/len(action_space) for _ in range(len(action_space))]
        self.policy[state] = policy
        return policy, action_space

    def update_policy(self, env: EnvNetwork, elite_session):
        new_policy = [[0] for _ in range(len(env.network.list_of_nodes))]

        for session in elite_session:
            print(f"session: {session}")
            for motion in session:
                reward, state, action, action_space = motion
                # print(f"new_policy {len(new_policy[state]), state, action}")
                num = self.search_action(env, action, action_space)
                new_policy[state] = [0 for _ in range(len(action_space))]
                new_policy[state][num] += 1

        for state in range(len(env.network.list_of_nodes)):
             # print(f"new_policy {len(new_policy), new_policy}")
            if len(new_policy[state]) == 1:
                neighbours = env.set_red_neighbours_nodes(env.network.list_of_nodes[state])
                default_action_space = env.set_red_action_space([env.network.list_of_nodes[state]] + neighbours)
                new_policy[state] = [0 for _ in range(len(default_action_space))]
            if sum(new_policy[state]) == 0:
                new_policy[state] = [1/len(new_policy[state]) for x in range(len(new_policy[state]))]
            elif sum(new_policy[state]) > 1:
                new_policy[state] /= sum(new_policy[state])

        print(f"Стандартная политика {self.policy} <-> Новая политика {new_policy}")
        self.policy = new_policy

    @staticmethod
    def search_action(env, action, action_space):
        for i in range(len(action_space)):
            if action_space[i] is action:
                return i
        print(f"Номер действия красного не найден!")


    def set_policy(self, env: EnvNetwork = None):
        self.policy = [0] * len(env.network.list_of_nodes)
        for i in range(len(env.network.list_of_nodes)):
            neighbours = env.set_red_neighbours_nodes(i)
            action_space = env.set_red_action_space([i] + neighbours)
            #print(f"Пространство действий коасного: {action_space}")
            self.policy[i] = [1/len(action_space) for x in range(len(action_space))]
