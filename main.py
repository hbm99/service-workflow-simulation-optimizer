import simpy
from environment import Product
from simulation import run_shop, profits_in_time
from fuzzy_logic import set_up_fuzzy_tip



def main():
    shop_size = 100
    num_cashiers = 20
    list_product = [Product('PIZZA', 10), Product('PAN', 5), Product('TOMATE', 3), Product('LECHUGA', 1), Product('JUGUETE', 20)]
    products = {item.name : item for item in list_product}
    simulation_time = 1000
    shelves_distribution = [1, 0, 1, 2, 3, 4, 4, 2, 3, 1, 0, 0]
    
    # Run the simulation
    env = simpy.Environment()
    tipping = set_up_fuzzy_tip(len(shelves_distribution))
    env.process(run_shop(env, num_cashiers, shop_size, products, shelves_distribution, tipping))
    env.run(until=simulation_time)



if __name__ == "__main__":
    main()
    print(profits_in_time[-1])



