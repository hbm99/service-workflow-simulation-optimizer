# from typing import List
# from customer import Customer, InAHurryCustomer

# from environment import ShopEnvironment


# class Simulation:
#     CUSTOMER_TYPE = [InAHurryCustomer]
#     def __init__(self, products : List[str], simulation_time : int, shop_environment : ShopEnvironment, shelves_distribution : List[int]) -> None:
#         self.products = products
#         self.shop_environment = shop_environment
#         self.shelves_distribution = shelves_distribution
#         self.simulation_time = simulation_time
    
#     def execute(self):
#         pass


import random
from typing import List
from customer import ConsumeristCustomer, InAHurryCustomer, RegularCustomer
from environment import Product, ShopEnvironment
import re
from customer_actions import ACTIONS

CUSTOMER_TYPES = [InAHurryCustomer, RegularCustomer, ConsumeristCustomer]

def run_shop(env, num_cashiers, shop_size, products, shelves_distribution):
    shop = ShopEnvironment(env, shop_size, products, shelves_distribution, num_cashiers)
    
    for id in range(3):
        customer = generate_customer(id, env, shop)
        env.process(go_shopping(env, customer, shop))
        
    while True:
        yield env.timeout(0.20)  # Wait a bit before generating a new customer
        
        id+=1
        customer = generate_customer(id, env, shop)
        env.process(go_shopping(env, customer, shop))

def go_shopping(env, customer, shop):
    
    planning = ["Go(0, 1)", "Take(pizza)", "Buy()"] # customer.get_plan() # ver cómo gestionar el tema de los tipos de clientes que su get_plan no devuelva los strings de planning
    
    for plan in planning:
        tokens = tokenize(plan)
        if tokens[0] == 'Buy':
            with shop.cashier.request() as request:
                yield request
                yield env.process(ACTIONS[tokens[0]](shop, customer, tokens[1:]).execute())
        else : yield env.process(ACTIONS[tokens[0]](shop, customer, tokens[1:]).execute())
        
    
def generate_customer(id, env, shop):
    random_index = random.randint(0, len(CUSTOMER_TYPES) - 1)
    shopping_list = fill_shopping_list(shop)
    arrival_time = env.now
    client = CUSTOMER_TYPES[random_index](id, arrival_time, shopping_list, shop)
    return client

def fill_shopping_list(shop):
    random.seed(45)
    products : List[Product] = list(shop.products.values())
    shopping_list = []
    len_shopping_list = random.randint(1, len(products))
    possible_indexes = [i for i in range(len(products))]

    for i in range(len_shopping_list):
        index = random.choice(possible_indexes)
        possible_indexes.pop(index)
        shopping_list.append(products[index])
    
    return shopping_list

def tokenize(plan : str):
    return re.findall(r"[\w']+", plan)
