from typing import List, Dict
import simpy


class Product:
    def __init__(self, name : str, price : int = 1) -> None:
        self.name = name
        self.price = price

class ShopEnvironment:
    def __init__(self, env, shop_size, products : Dict[str, Product], shelves_distribution : List[int], num_cashiers : int = 1):
        self.env = env
        self.profit = 0
        self.cashier = simpy.Resource(env, num_cashiers)
        self.products = products
        
        self.sections = []
        for i in range(len(shelves_distribution)):
            self.sections.append(Section(products[list(products.keys())[shelves_distribution[i]]], i))
        
        self.cashiers = []
        for i in range(num_cashiers):
            self.cashiers.append(Cashier())
        
        self.init_map(shop_size)
        
    
    def init_map(self, shop_size):
        self.map = [[None] * shop_size] * shop_size
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                self.map[i][j] = Cell((i, j))
        self.insert_sections()
        self.insert_cashiers()
        
    def insert_cashiers(self):
        cashiers_index = 0
        for i in range(2, len(self.map), 2):
            cashier = self.cashiers[cashiers_index]
            cashier.position = (i, 0)
            self.map[i][0] = cashier
            cashiers_index+=1
            if cashiers_index == len(self.cashiers):
                return
    
    def insert_sections(self):
        sections_index = 0
        for i in range(2, len(self.map), 2):
            for j in range(2, len(self.map[0])):
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
    def __init__(self, product : Product, index : int) -> None:
        super().__init__()
        self.product = product
        self.index_in_sections = index

class Cashier(Cell):
    def __init__(self) -> None:
        super().__init__()
        

