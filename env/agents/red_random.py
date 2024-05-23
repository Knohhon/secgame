import numpy as np

from env.agents.red_agent import RedAgent


class RedRandomAgent(RedAgent):
    def __init__(self, list_states_actions):
        super().__init__()
        self.agent = RedAgent()
        self.list_states_actions = list_states_actions
        self.agent.red_policy = np.ones(list_states_actions[0], list_states_actions[1]) / list_states_actions[1]

    def get_action(self, state):
        prob = self.agent.red_policy[state]
        action = np.random.choice(np.arange(self.agent.action), p=prob)
        return action

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


