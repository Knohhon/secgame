#TODO: Deprecated?

class AgentInterface:
    """
    Интерфейс доступа к параметрам синич агентов
    """

    def __init__(self):
        self.__state = None
        self.__policy = None
        self.__action = None

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state):
        self.__state = state

    @property
    def policy(self):
        return self.__policy

    @policy.setter
    def policy(self, policy):
        self.__policy = policy

    @property
    def action(self):
        return self.__action

    @action.setter
    def action(self, action):
        self.__action = action
