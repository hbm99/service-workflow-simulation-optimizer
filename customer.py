from abc import ABC, abstractmethod
import random
from typing import List

from sympy import false, true
from environment import Product, ShopEnvironment, Section
from costumer_utlils import dfs


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
    def __init__(self, id : int, arrival_time : int, shopping_list : List[Product], shop_environment : ShopEnvironment, start_position : tuple = (0, 0), money : int = 10**10, time : int = 10**10):
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
    
    def update_current_section(self, section_position):
        i, j = section_position
        self._current_section = self._shop_environment.map[i][j]

    @abstractmethod
    def get_plan(self):
        """
        Returns actions for buying stuff from the shopping list.
        """
        pass

    @abstractmethod
    def take(self, product : Product):
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
        Goes to random cashier for payment and spends money.
        """
        selected_cashier_index = random.randint(0, len(self._shop_environment.cashiers) - 1)
        
        self.go(self._current_section.position, self._shop_environment.cashiers[selected_cashier_index].position)
        
        # waiting until the selected cashier gets free
        while self._shop_environment.cashiers[selected_cashier_index].client_count == 1:
            yield self._shop_environment.env.timeout(3)
            
        self._shop_environment.cashiers[selected_cashier_index].client_count+=1
        
        yield self._shop_environment.env.timeout(random.randint(len(self._products_cart) * 2, len(self._products_cart) * 5))
        
        self._shop_environment.profit+=sum([product.price for product in self._products_cart])
        
        self._shop_environment.cashiers[selected_cashier_index].client_count-=1
        
class InAHurryCustomer(Customer):
    def __init__(self, id: int, arrival_time: int, shopping_list: List[Product], shop_environment: ShopEnvironment, start_position: tuple = (0, 0), money: int = 10 ** 10, time: int = 10 ** 10):
        super().__init__(id, arrival_time, shopping_list, shop_environment, start_position, money, time)
    def get_plan(self):
        # Insert your code here
        pass
    def take(self, product: Product):
        # Insert your code here
        yield self._shop_environment.env.timeout(random.randint(1, 3))
        # Insert your code here
    def go(self, a: tuple, b: tuple):
        # Insert your code here
        yield self._shop_environment.env.timeout(random.randint(1, 3))
        self.update_current_section(b)
        # Insert your code here
    
class ConsumeristCustomer(Customer):
    def __init__(self, id: int, arrival_time: int, shopping_list: List[Product], shop_environment: ShopEnvironment, start_position: tuple = (0, 0), money: int = 10 ** 10, time: int = 10 ** 10):
        super().__init__(id, arrival_time, shopping_list, shop_environment, start_position, money, time)
    def get_plan(self):
        # Insert your code here
        pass
    def take(self, product: Product):
        # Insert your code here
        yield self._shop_environment.env.timeout(random.randint(1, 3))
        # Insert your code here
    def go(self, a: tuple, b: tuple):
        # Insert your code here
        yield self._shop_environment.env.timeout(random.randint(1, 3))
        self.update_current_section(b)
        # Insert your code here


#######################################################3
from planning.get_plan import shopping_problem

class RegularCustomer(Customer):
    def __init__(self, id: int, arrival_time: int, shopping_list: List[Product], 
                    shop_environment: ShopEnvironment, start_position: tuple = (0, 0), 
                        money: int = 10 ** 10, time: int = 10 ** 10):

        super().__init__(id, arrival_time, shopping_list, shop_environment, start_position, money, time)

    def get_plan(self) -> list(str):
        planification = shopping_problem(self, self.shop_environment)
        return planification.append("Buy()")

    def take(self, product: Product):
        # Insert your code here
        yield self._shop_environment.env.timeout(random.randint(1, 3))
        self._products_cart.append(product)
        self._shopping_list.pop()

    def go(self, a: tuple, b: tuple):
        # Reduce in one, de client count of the cell
        map = self._shop_environment.map[a[0]][a[1]].client_count - 1
        path = dfs(map, a, b)
        #TODO Devolver path?
        yield self._shop_environment.env.timeout(random.randint(1, 3))
        self.update_current_section(b)
        # Insert your code here

 



