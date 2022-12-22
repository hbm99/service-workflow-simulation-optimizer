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


from customer import Customer
from environment import ShopEnvironment
import re
from customer_actions import ACTIONS

def run_shop(env, num_cashiers, shop_size, products, shelves_distribution):
    shop = ShopEnvironment(env, shop_size, products, shelves_distribution, num_cashiers)
    
    for customer in range(3):
        customer = generate_customer(env, shop)
        env.process(go_shopping(env, customer, shop))
        
    while True:
        yield env.timeout(0.20)  # Wait a bit before generating a new customer

        customer = generate_customer(env, shop)
        env.process(go_shopping(env, customer, shop))

def go_shopping(env, customer, shop):
    
    arrival_time = env.now
    
    planning = ["Go(0, 1)"]#customer.get_plan()
    
    for plan in planning:
        tokens = tokenize(plan)
        if tokens[0] == 'Buy':
            with shop.cashier.request() as request:
                yield request
                yield env.process(ACTIONS[tokens[0]](shop, customer, tokens[1:]).execute())
        else : yield env.process(ACTIONS[tokens[0]](shop, customer, tokens[1:]).execute())
            
    
    # with shop.cashier.request() as request:
    #     yield request
    #     yield env.process(theater.purchase_ticket(moviegoer))

    # with theater.usher.request() as request:
    #     yield request
    #     yield env.process(theater.check_ticket(moviegoer))

    # if random.choice([True, False]):
    #     with theater.server.request() as request:
    #         yield request
    #         yield env.process(theater.sell_food(moviegoer))

    # # Moviegoer heads into the theater
    # wait_times.append(env.now - arrival_time)
    
def generate_customer(env, shop):
    return Customer(env.now, {}, shop)

def tokenize(plan : str):
    return re.findall(r"[\w']+", plan)
