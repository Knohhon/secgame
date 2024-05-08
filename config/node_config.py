#TODO: добавить имя и тип узлов

class NodeConfig:
    def __init__(self, compromise_point: bool, compromise_speed: bool, perfomance_points: bool):
        self.compromise_point = compromise_point
        self.compromise_speed = compromise_speed
        self.perfomance_points = perfomance_points

