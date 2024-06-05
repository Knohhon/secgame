import numpy as np

from env.agents.agent_interface import AgentInterface
from env.envNetwork import EnvNetwork


class RedRandomAgent(AgentInterface):
    def __init__(self, ):
        super().__init__()
        self.policy = None

    def get_action(self, state, env: EnvNetwork = None) -> list[int, int, int]:
        prob = self.policy[state]
        print(prob, env.red_action_space)
        action = np.random.choice(len(env.red_action_space), p=prob)
        if env.red_action_space[action][2] == 2 and env.red_action_space[action][2] in env.attacks:
            self.get_action(state, env)
        elif env.red_action_space[action] == 3 and env.red_action_space[action][2] not in env.attacks:
            self.get_action(state, env)

        return env.red_action_space[action]

    """
    def update_policy(self, elite_session):
        new_policy = np.zeros(self.list_states_actions[0], self.list_states_actions[1])

        for session in elite_session:
            for state, action in (session['state'], session['action']):
                new_policy[state][action] += 1

        for state in range(self.list_states_actions[0]):
            if new_policy[state] == 0:
                new_policy[state] = 1 / self.list_states_actions[1]
            else:
                new_policy[state] /= new_policy[state]

        self.policy = new_policy
    """

    def set_policy(self, env: EnvNetwork = None):
        self.policy = [0] * len(env.network.list_of_nodes)
        for i in range(len(env.network.list_of_nodes)):
            neighbours = env.set_red_neighbours_nodes(i)
            action_space = env.set_red_action_space([i] + neighbours)
            #print(f"Пространство действий коасного: {action_space}")
            self.policy[i] = [1/len(action_space) for x in range(len(action_space))]

