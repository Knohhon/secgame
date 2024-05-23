class NetworkConfig:
    def __init__(self, node_count: int, edge_count: int, random_edges: bool, count_layers: int):
        self.__node_count = node_count
        self.__edge_count = edge_count
        self.__random_edges = random_edges
        self.__count_layers = count_layers

    @property
    def node_count(self):
        return self.__node_count

    @node_count.setter
    def node_count(self, value):
        self.__node_count = value

    @property
    def edge_count(self):
        return self.__edge_count

    @edge_count.setter
    def edge_count(self, value):
        self.__edge_count = value

    @property
    def random_edges(self):
        return self.__random_edges

    @random_edges.setter
    def random_edges(self, value):
        self.__random_edges = value

    @property
    def count_layers(self) -> int:
        return int(self.__count_layers)

    @count_layers.setter
    def count_layers(self, value):
        self.__count_layers = value
