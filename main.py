import random
import simpy
from environment import Product
from simulation import run_shop



def main():
    random.seed(42)
    shop_size = 8
    num_cashiers = 1
    products = [Product('pizza', 10), Product('pan', 5)]
    simulation_time = 4
    shelves_distribution = [1, 0, 1]
    
    # Run the simulation
    env = simpy.Environment()
    env.process(run_shop(env, num_cashiers, shop_size, products, shelves_distribution))
    env.run(until=simulation_time)
    
    
    


if __name__ == "__main__":
    main()



