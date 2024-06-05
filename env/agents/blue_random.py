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

    """
    def update_policy(self, elite_session):
        new_policy = np.zeros(self.state[0], self.state[1])

        for session in elite_session:
            for state, action in (session['state'], session['action']):
                new_policy[state][action] += 1

        for state in range(self.list_states_actions[0]):
            if new_policy[state] == 0:
                new_policy[state] = 1 / self.list_states_actions[1]
            else:
                new_policy[state] /= new_policy[state]

        self.blue_policy = new_policy
    """

    @staticmethod
    def interpretate_state(env: EnvNetwork = None) -> int:
        s = 0
        for i in range(len(env.network.list_of_nodes)):
            for j in range(len(env.blue_action_var) + 1):
                s += 1
        return s

    def set_policy(self, env: EnvNetwork = None):
        print(env.network.list_of_nodes)
        print(self.interpretate_state(env))
        self.policy = [0] * self.interpretate_state(env)
        for i in range(self.interpretate_state(env)):
            self.policy[i] = [1/len(env.blue_action_space) for x in range(len(env.blue_action_space))]



