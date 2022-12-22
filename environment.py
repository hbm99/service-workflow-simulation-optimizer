from abc import ABC
from joblib import Parallel
from typing import List
import simpy

class ShopEnvironment:
    def __init__(self, env, shop_size, products : List[str], shelves_distribution : List[int], num_cashiers : int):
        self.env = env
        self.cashier = simpy.Resource(env, num_cashiers)
        # sections splitting the shop
        self.sections = []
        for i in range(len(shelves_distribution)):
            self.sections.append(Section(products[shelves_distribution[i]], i))
        

        # list of cashiers at the shop
        # self.cashier = [ParallelServer() for i in range(server_count)]
        
        
        self.init_map(shop_size)
        
    
    def init_map(self, shop_size):
        self.map = [[None] * shop_size] * shop_size
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                self.map[i][j] = Cell((i, j))
        self.insert_sections(shop_size)
    
    def insert_sections(self, shop_size):
        spaces = shop_size / len(self.sections)
        sections_index = 0
        for i in range(1, len(self.map), 2):
            for j in range(1, len(self.map[0])):
                section = self.sections[sections_index]
                section.position = (i, j)
                self.map[i][j] = section
                sections_index += 1
                if sections_index == len(self.sections):
                    return

class Cell:
    def __init__(self, position : tuple = (-1, -1)) -> None:
        self.client_count = 0
        self.position = position

class Section(Cell):
    def __init__(self, product, index):
        super().__init__()
        self.product = product
        self.index_in_sections = index

class Cashier(Cell):
    def __init__(self) -> None:
        super().__init__()


class ParallelServer():
    pass
