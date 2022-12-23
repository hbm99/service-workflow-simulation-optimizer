from abc import ABC, abstractmethod
import random
from typing import Dict
from environment import Product, ShopEnvironment, Section


class Customer(ABC):
    _arrival_time = 0
    _shopping_list = {Section : int}
    _shop_environment = None
    _position = None
    _products_cart = []
    _money = 0
    _current_section = None
    _buying_time = 0
    
    @abstractmethod
    def __init__(self, id : int, arrival_time : int, shopping_list : Dict[Product], shop_environment : ShopEnvironment, start_position : tuple = (0, 0), money : int = 10**10, time : int = 10**10):
        self.id = id
        self._arrival_time = arrival_time
        self._shopping_list = shopping_list
        self._shop_environment = shop_environment
        self._position = start_position
        self._products_cart = []
        self._money = money
        self._buying_time = time
        
    
    def get_products_cart(self):
        """
        Returns customer products to buy.
        """
        return self._products_cart
    
    def get_arrival_time(self):
        """
        Returns customer arrival time.
        """
        return self._arrival_time
    
    def get_shopping_list(self):
        """
        Returns customer shopping list.
        """
        return self._shopping_list
    
    @abstractmethod
    def get_plan(self):
        """
        Returns actions for buying stuff from the shopping list.
        """
        pass

    @abstractmethod
    def take(self, product : int, section : Section):
        """
        Reduces shopping list by decrementing taken article and add to product car.
        """
        pass
        #self._shopping_list.pop(product)
    
    @abstractmethod
    def go(self, a : tuple, b: tuple):
        """
        Moves from section A to section B.
        """
        pass
    
    def buy(self):
        """
        Goes to cashier for payment and spends money.
        """
        self.go(self._current_section.position, self._shop_environment.cashiers[random.randint(0, len(self._shop_environment.cashiers) - 1)].position)
        
        yield self._shop_environment.env.timeout(random.randint(len(self._products_cart) * 2, len(self._products_cart) * 5))
        
        self._shop_environment.profit+=sum([product.price for product in self._products_cart])
        
class InAHurryCustomer(Customer):
    def __init__(self, id: int, arrival_time: int, shopping_list: Dict[Product], shop_environment: ShopEnvironment, start_position: tuple = (0, 0), money: int = 10 ** 10, time: int = 10 ** 10):
        super().__init__(id, arrival_time, shopping_list, shop_environment, start_position, money, time)
    def get_plan(self):
        # Insert your code here
        pass
    def take(self, product: int, section: Section):
        # Insert your code here
        pass
    def go(self, a: tuple, b: tuple):
        # Insert your code here
        pass
    
class ConsumeristCustomer(Customer):
    def __init__(self, id: int, arrival_time: int, shopping_list: Dict[Product], shop_environment: ShopEnvironment, start_position: tuple = (0, 0), money: int = 10 ** 10, time: int = 10 ** 10):
        super().__init__(id, arrival_time, shopping_list, shop_environment, start_position, money, time)
    def get_plan(self):
        # Insert your code here
        pass
    def take(self, product: int, section: Section):
        # Insert your code here
        pass
    def go(self, a: tuple, b: tuple):
        # Insert your code here
        pass
    
class RegularCustomer(Customer):
    def __init__(self, id: int, arrival_time: int, shopping_list: Dict[Product], shop_environment: ShopEnvironment, start_position: tuple = (0, 0), money: int = 10 ** 10, time: int = 10 ** 10):
        super().__init__(id, arrival_time, shopping_list, shop_environment, start_position, money, time)
    def get_plan(self):
        # Insert your code here
        pass
    def take(self, product: int, section: Section):
        # Insert your code here
        pass
    def go(self, a: tuple, b: tuple):
        # Insert your code here
        pass