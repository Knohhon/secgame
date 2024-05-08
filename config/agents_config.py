from random import randint

#TODO перенести AgentConfig в класс создания агента


class AgentConfig:
    def __init__(self, agent_type, agent_id):
        self.__agent_type = agent_type
        self.__agent_id = agent_id

    @property
    def agent_type(self):
        return self.__agent_type

    @property
    def agent_id(self):
        return self.__agent_id

    @classmethod
    def set_agent_id(cls, agent_id):
        agent_id = randint(0, 100)
        cls.__agent_id = agent_id


class RedAgentConfig:
    def __init__(self, replace_to_node: bool, compromise: bool):
        self.__red_replace_to_node = replace_to_node
        self.__red_compromise = compromise

    @property
    def red_replace_to_node(self):
        return self.__red_replace_to_node

    @red_replace_to_node.setter
    def red_replace_to_node(self, value):
        self.__red_replace_to_node = value

    @property
    def red_compromise(self):
        return self.__red_compromise

    @red_compromise.setter
    def red_compromise(self, value):
        self.__red_compromise = value


class BlueAgentConfig:
    def __init__(self, close_node: bool, repare: bool):
        self.__blue_close_node = close_node
        self.__blue_repare = repare

    @property
    def blue_close_node(self):
        return self.__blue_close_node

    @blue_close_node.setter
    def blue_close_node(self, value):
        self.__blue_close_node = value

    @property
    def blue_repare(self):
        return self.__blue_repare

    @blue_repare.setter
    def blue_repare(self, value):
        self.__blue_repare = value
