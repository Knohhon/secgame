from env.agents.agent_interface import AgentInterface
from env.envNetwork import EnvNetwork


class BlueSimpleMaxAgent(AgentInterface):
    def __init__(self):
        super().__init__()

    def get_action(self, env: EnvNetwork, observation):
        mx = 0
        num_max = 0
        for i in range(len(observation[0])):
            if observation[i][i] > mx:
                mx = observation[i][i]
                num_max = i
        action = self.choose_action(env, num_max)
        return action

    @staticmethod
    def choose_action(env: EnvNetwork, num_max):
        if num_max not in env.defenses:
            return [num_max, 0]
        elif num_max in env.defenses:
            return [num_max, 1]
