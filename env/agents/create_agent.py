from env.agents.blue_random import BlueRandomAgent
from env.agents.blue_simple_max import BlueSimpleMaxAgent
from env.agents.red_random import RedRandomAgent


class Agent:
    """
    Реализует функциию создания агента.
    :argument agent_type: tuple[str, str] = None, options: list = None
    """

    def __init__(self, agent_type: tuple[str, str] = None, options: list = None):
        self.agent_type = agent_type
        self.ready_types = {"Red": ["Random"], "Blue": ["Random"]}
        self.options = options

    def create_agent(self):
        try:
            self.agent_type is None
        except ValueError:
            raise ValueError(f"Agent type is None: {self.agent_type}")

        try:
            (self.agent_type[0] not in self.ready_types
             or self.agent_type[1] not in self.ready_types.get(self.agent_type[0]))
        except ValueError:
            raise ValueError(f"Agent type must be in {self.ready_types}")

        try:
            len(self.options) > 0
        except ValueError:
            raise ValueError(f"Options must be added: {self.ready_types}")

        if self.agent_type[0] == "Red":
            if self.agent_type[1] == "Random":
                return RedRandomAgent()
            else:
                return "Oops!"
        elif self.agent_type[0] == "Blue":
            if self.agent_type[1] == "Random":
                return BlueRandomAgent()
            elif self.agent_type[1] == "SimpleMax":
                return BlueSimpleMaxAgent()
            else:
                return "Oops!"
