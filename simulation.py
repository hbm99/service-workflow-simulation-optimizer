import random
import re
from typing import List

from customer import ConsumeristCustomer, InAHurryCustomer, RegularCustomer
from customer_actions import ACTIONS
from environment import Product, ShopEnvironment


tips_in_time = []
peolple_at_section = []
profits_in_time = []

CUSTOMER_TYPES = [ConsumeristCustomer, InAHurryCustomer, RegularCustomer] # pending add regular customer

def run_shop(env, num_cashiers, shop_size, products, shelves_distribution, tipping):

    shop = ShopEnvironment(env, shop_size, products, shelves_distribution, num_cashiers)
    
    for id in range(3):
        customer = generate_customer(id, env, shop)
        env.process(go_shopping(env, customer, shop, tipping))
    
   
    while True:
        yield env.timeout(random.randint(30, 150))  # Wait a bit before generating a new customer
        
        id+=1
        customer = generate_customer(id, env, shop)
        env.process(go_shopping(env, customer, shop, tipping))
    

        peolple_at_section.append([section.client_count for section in shop.sections])

    

def go_shopping(env, customer, shop, tipping):
    
    planning = customer.get_plan()

    for plan in planning:
        tokens = tokenize(plan)
        if tokens[0] == 'Buy':
            with shop.cashier.request() as request:
                yield request
                yield env.process(ACTIONS[tokens[0]](shop, customer, tokens[1:]).execute())
                
                profits_in_time.append(shop.profit)
                
                spended = sum([product.price for product in customer._products_cart])

                # Tip logic
                tipping.input['people_count'] = customer._people_perceived_at_shop
                tipping.compute()

                tip_percent = tipping.output['tip']
                tip = int(round(tip_percent * (spended/100), 2))
                
                tips_in_time.append(tip)

                profits_in_time[-1] += tip
                
                shop.profit += tip
                
                print(f"    {str(customer)} spent ${spended} and left a tip of ${tip}")  
                print(f"    Total profit: ${profits_in_time[-1]}")
                

        else : yield env.process(ACTIONS[tokens[0]](shop, customer, tokens[1:]).execute())
        
        
    
def generate_customer(id, env, shop):
    shopping_list = fill_shopping_list(shop)
    arrival_time = env.now
    client_type = random.choice(CUSTOMER_TYPES)
    client = client_type(id, arrival_time, shopping_list, shop)
    return client

def fill_shopping_list(shop):
    products : List[Product] = list(shop.products.values())
    shopping_list = []
    len_shopping_list = random.randint(1, len(products))
    possible_indexes = [i for i in range(len(products))]

    for i in range(len_shopping_list):
        index_value = random.choice(possible_indexes)
        possible_indexes.remove(index_value)
        shopping_list.append(products[index_value])
    
    return shopping_list

def tokenize(plan : str):
    return re.findall(r"[\w']+", plan)
