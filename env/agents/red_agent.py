class RedAgent:
    def __init__(self, red_state, red_policy, red_action):
        self.red_state = red_state
        self.red_policy = red_policy
        self.red_action = red_action

    @property
    def state(self):
        return self.red_state

    @state.setter
    def state(self, state):
        self.red_state = state

    @property
    def policy(self):
        return self.red_policy

    @policy.setter
    def policy(self, policy):
        self.red_policy = policy

    @property
    def action(self):
        return self.red_action

    @action.setter
    def action(self, action):
        self.red_action = action


