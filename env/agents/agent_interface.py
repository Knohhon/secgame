from env.agents.create_agent import Agent


class BlueAgent():
    def __init__(self, agent_type: str):
        self.blue_state = None
        self.blue_policy = None
        self.blue_action = None

    @property
    def state(self):
        return self.blue_state

    @state.setter
    def state(self, state):
        self.blue_state = state

    @property
    def policy(self):
        return self.blue_policy

    @policy.setter
    def policy(self, policy):
        self.blue_policy = policy

    @property
    def action(self):
        return self.blue_action

    @action.setter
    def action(self, action):
        self.blue_action = action
