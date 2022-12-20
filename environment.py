from abc import ABC
from joblib import Parallel
from typing import List

class ShopEnvironment:
    def __init__(self, shop_size, section_names : List[str], server_count : int):
        # sections splitting the shop
        self.sections = {}
        for name in section_names:
            self.sections[name] = Section(name)

        # list of cashiers at the shop
        # self.cashier = [ParallelServer() for i in range(server_count)]
        
        self.map = [["None"] * shop_size] * shop_size
        # self.fill_initial_map()
        
    def fill_initial_map(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                self.map[i][j] = Cell()

class Cell:
    def __init__(self) -> None:
        self.client_count = 0

class Section(Cell):
    def __init__(self, name):
        super().__init__()
        self.name = name

class Cashier(Cell):
    def __init__(self) -> None:
        super().__init__()


class ParallelServer():
    pass
