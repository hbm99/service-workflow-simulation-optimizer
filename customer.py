from abc import ABC, abstractmethod
import random
from typing import List

from sympy import false, true
from environment import Product, ShopEnvironment, Section

from planning.get_plan import get_planning, shopping_problem

from environment import Product, ShopEnvironment
from walking_problem.heuristic_problem_utils import astar_search, path_actions
from walking_problem.walking_problem_utils import WalkingProblem, depth_first_search
import utils


class Customer(ABC):
    @abstractmethod
    def __init__(self, id : int, arrival_time : int, shopping_list : List[Product], shop_environment : ShopEnvironment, start_position : tuple = (0, 0), money : int = 10**10, time : int = 10**10):
        self.id = id
        self._arrival_time = arrival_time
        self._shopping_list = shopping_list
        self._shop_environment = shop_environment
        self._position = start_position
        self._current_section = None
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

class AStarGoCustomer(Customer):
    def go(self, a: tuple, b: tuple):
        if self._current_section is not None:
            self._current_section.client_count-=1
        walking_problem = WalkingProblem(a, [b], shop_map = self._shop_environment.map)
        solution = astar_search(walking_problem)
        walking_time = len(path_actions(solution))
        yield self._shop_environment.env.timeout(walking_time)
        self.update_current_section(b)
        self._current_section.client_count+=1

class InAHurryCustomer(AStarGoCustomer):
    def __init__(self, id: int, arrival_time: int, shopping_list: List[Product], shop_environment: ShopEnvironment, start_position: tuple = (0, 0), money: int = 10 ** 10, time: int = 10 ** 10):
        super().__init__(id, arrival_time, shopping_list, shop_environment, start_position, money, time)
    
    def get_plan(self):
        """
        Gets a greedy plan depending on clients count in sections.
        """
        # get sections with shopping list products
        sections_list = []
        for section in self._shop_environment.sections:
            if section.product in self._shopping_list:
                sections_list.append(section)
        
        # remove duplicated sections
        for i in range(len(sections_list)):
            for j in range(len(sections_list)):
                if i == j:
                    continue
                if sections_list[i] == sections_list[j]:
                    sections_list.pop(j)
        
        # order by sections'clients_count
        sections_list.sort(key=self.clients_in_section)
        
        # build str(plan)
        plan = ["Go("+ str(sections_list[0].index_in_sections) + ")"]
        previous_section = sections_list[0]
        
        for i in range(1, len(sections_list)):
            
            section = sections_list[i]
            
            go_action = "Go("+ str(previous_section.index_in_sections) + ","+ str(section.index_in_sections)+ ")"
            previous_section = section
            plan.append(go_action)

            take_action = "Take("+ section.product.name + ")"
            plan.append(take_action)
        
        buy_action = "Buy()"
        plan.append(buy_action)
        
        return plan
                
    def clients_in_section(self, section):
        return section.client_count
        
    
    def take(self, product: Product):
        if self._current_section.client_count > 15:  #hurry client => if there is too much people in section, doesn't buy article!!
            return
        yield self._shop_environment.env.timeout(random.randint(1, 3))
        self._products_cart.append(product)
        self._shopping_list.remove(product)
        
    def __str__(self) -> str:
        return str(self.id) + ': InAHurryCustomer'
        
    
class ConsumeristCustomer(AStarGoCustomer):
    def __init__(self, id: int, arrival_time: int, shopping_list: List[Product], shop_environment: ShopEnvironment, start_position: tuple = (0, 0), money: int = 10 ** 10, time: int = 10 ** 10):
        super().__init__(id, arrival_time, shopping_list, shop_environment, start_position, money, time)
    def get_plan(self):

        planning=["Go("+ str(0)+ ")"]

        prev_section= self._shop_environment.sections[0]
        aux_shopping_list= self._shopping_list

        for i in range(1,len(self._shop_environment.sections)):
            sec= self._shop_environment.sections[i]
            
            # Go action
            action= "Go("+ str(prev_section.index_in_sections) + ","+ str(sec.index_in_sections)+ ")"
            prev_section= sec
            planning.append(action)

            # Take action
            extra_product = random.random()
            product_founded = prev_section.product in aux_shopping_list
            if(extra_product > 0.6 or product_founded):
                action= "Take("+ sec.product.name + ")"
                if(product_founded): aux_shopping_list.remove(prev_section.product)
            planning.append(action)

        # Buy action
        action= "Buy()"
        planning.append(action)

        return planning
        
    def take(self, product: Product):

        yield self._shop_environment.env.timeout(random.randint(1, 3 + 2 * (self._current_section.client_count-1)))
        if product in self._shopping_list:
            self._shopping_list.remove(product)
        self._products_cart.append(product)
        
    def __str__(self) -> str:
        return str(self.id) + ': ConsumeristCustomer'
        

class RegularCustomer(Customer):
    def __init__(self, id: int, arrival_time: int, shopping_list: List[Product], 
                    shop_environment: ShopEnvironment, start_position: tuple = (0, 0), 
                        money: int = 10 ** 10, time: int = 10 ** 10):

        super().__init__(id, arrival_time, shopping_list, shop_environment, start_position, money, time)

    def get_plan(self):
        problem = shopping_problem(self, self._shop_environment)
        planification = get_planning(problem)
        planification.append("Buy()")
        return planification

    def take(self, product: Product):
        
        yield self._shop_environment.env.timeout(random.randint(1, 3 + 1 * (self._current_section.client_count-1)))
        self._shopping_list.remove(product)
        self._products_cart.append(product)


    def go(self, a: tuple, b: tuple):
        self._shop_environment.map[a[0]][a[1]].client_count - 1
        map = self._shop_environment.map
        path = depth_first_search(map, a, b)

        yield self._shop_environment.env.timeout(random.randint(1, 3))
        self.update_current_section(b)
        return path


    def __str__(self) -> str:
        return str(self.id) + ': RegularCustomer'
