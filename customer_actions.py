from abc import ABC, abstractmethod
from customer import Customer
from environment import Cell, ShopEnvironment
#from typing import List


class CustomerAction(ABC):
    
    @abstractmethod
    def execute(self):
        pass
        
    
class Go(CustomerAction):
    def __init__(self, shop : ShopEnvironment, customer : Customer, args) -> None:
        self.shop = shop
        self.customer = customer
        self.args = args
    
    def execute(self):
        index_start = int(self.args[0])
        index_goal = int(self.args[1])
        start : Cell = self.shop.sections[index_start]
        goal : Cell = self.shop.sections[index_goal]
        return self.customer.go(start.position, goal.position)
        
        
class Buy:
    def __init__(self) -> None:
        pass
        
class Take:
    def __init__(self) -> None:
        pass
        
ACTIONS = {'Go' : Go, 'Take' : Take, 'Buy' : Buy}