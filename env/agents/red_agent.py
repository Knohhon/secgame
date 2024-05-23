class RedAgent:
    def __init__(self):
        self.red_state = None
        self.red_policy = None
        self.red_action = None

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


