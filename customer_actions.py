from abc import ABC, abstractmethod
from customer import Customer
from environment import Cell, ShopEnvironment


class CustomerAction(ABC):
    @abstractmethod
    def __init__(self, shop : ShopEnvironment, customer : Customer, args) -> None:
        self.shop = shop
        self.customer = customer
        self.args = args
    
    @abstractmethod
    def execute(self):
        pass
        
    
class Go(CustomerAction):
    def __init__(self, shop: ShopEnvironment, customer: Customer, args) -> None:
        super().__init__(shop, customer, args)
    
    def execute(self):
        if len(self.args) == 1:
            goal : Cell = self.shop.sections[int(self.args[0])]
            start_position = (0, 0)
            return self.customer.go(start_position, goal.position)

        index_start = int(self.args[0])
        index_goal = int(self.args[1])
        start : Cell = self.shop.sections[index_start]
        goal : Cell = self.shop.sections[index_goal]
        return self.customer.go(start.position, goal.position)
        
        
class Buy(CustomerAction):
    def __init__(self, shop: ShopEnvironment, customer: Customer, args) -> None:
        super().__init__(shop, customer, args)
    
    def execute(self):
        return self.customer.buy()
        
class Take(CustomerAction):
    def __init__(self, shop: ShopEnvironment, customer: Customer, args) -> None:
        super().__init__(shop, customer, args)
        
    def execute(self):
        return self.customer.take(self.shop.products[self.args[0]])
        
ACTIONS = {'Go' : Go, 'Take' : Take, 'Buy' : Buy}