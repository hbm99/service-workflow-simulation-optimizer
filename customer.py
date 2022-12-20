from abc import ABC, abstractmethod
from environment import ShopEnvironment, Section
from walking_problem.walking_problem_utils import breadth_first_search


class Customer(ABC):
    _arrival_time = 0
    _shopping_list = {Section: int}
    _shop_environment = None
    _position = None
    _products_cart = []
    _money = 0
    _current_section = None
    _buying_time = 0
    
    @abstractmethod
    def __init__(self, arrival_time : int, shopping_list : dict, shop_environment : ShopEnvironment, start_position : tuple = (0, 0), money : int = 10**10, time : int = 10**10):
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
    
    def take(self, product_section):# : Section):
        """
        Reduces shopping list by decrementing taken article.
        """
        self._shopping_list.pop(product_section)
        
        # product_amount = self._shopping_list[product] # when clients buy specific products amount (next gen project)
        # if product_amount > 1:
        #     product_amount-= 1
        # else: 
        #     self._shopping_list.pop(product)
            
        # self._shop_environment.sections[product_section].products_count-= 1 (next gen project)
        
    def go(self, a : tuple, b: tuple):
        """
        Moves from section A to section B.
        """
        # call bfs from utils.py when bfs is adapted
        road = breadth_first_search(self._shop_environment.map, a, b)
        self._current_section = self._shop_environment.map[b]
        # return road
        
    def buy(self):
        """
        Goes to cashier for payment and spends money.
        """
        # self.go(self._current_section.position, self._shop_environment.cashiers[random or closer or empty].position)
        
        # spending_money = 0
        # for section in self._products_cart:
        #     spending_money += section.price
        
        # self._money -= spending_money (next gen project)
        
class InAHurryCustomer(Customer):
    pass