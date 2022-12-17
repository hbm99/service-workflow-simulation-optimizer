from abc import ABC
from joblib import Parallel
from typing import List

class ShopEnviroment:
    def __init__(self, shop_size, sections_names : List[str], server_count : int):
        # sections list splitting the shop
        self.sections = {}
        for name in sections_names:
            self.sections[name] = Section(name)

        # list of cashiers at the shop
        self.cashier = [ParallelServer() for i in range(server_count)]
        
        self.map = [["None"] * shop_size] * shop_size
        # self.fill_initial_map()
        
    def fill_initial_map(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                self.map[i][j] = Cell((i, j))

class Cell:
    def __init__(self, pos) -> None:
        # self.position = pos
        pass

class Section(Cell):
    def __init__(self, name):
        self.name = name
        self.client_count = 0

class ParallelServer():
    pass

class Cashier:
    def __init__(self) -> None:
        pass

