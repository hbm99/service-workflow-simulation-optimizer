import random
import simpy



def main():
    random.seed(42)
    shop_size = 8
    num_cashiers = 1
    products = ['pizza', 'pan']
    simulation_time = 500
    shelves_distribution = [1, 2, 1]
    
    # Run the simulation
    env = simpy.Environment()
    env.process(run_shop(env, num_cashiers, shop_size, products, shelves_distribution))
    env.run(until=simulation_time)
    
    
    


if __name__ == "__main__":
    main()



