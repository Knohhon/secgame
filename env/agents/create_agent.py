class Agent:
    def __init__(self, agent_type=None):
        if agent_type is None:
            agent_type = ["Red", "Blue"]
        self.agent_type = ""
