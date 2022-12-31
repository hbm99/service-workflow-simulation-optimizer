import simpy
from environment import Product
from simulation import run_shop, profits_in_time, peolple_at_section, tips_in_time
from fuzzy_logic import set_up_fuzzy_tip


def main(size, cashiers, time, customers):
    shop_size = size
    num_cashiers = cashiers
    customer_types = customers
    list_product = [Product('Pizza', 10), Product('Pan', 5), Product('Tomate', 3), Product('Jugo', 3), Product('Pan', 3), Product('Cerveza', 3)]
    products = {item.name : item for item in list_product}
    simulation_time = time
    shelves_distribution = [0, 0, 3, 4, 2, 6, 4, 4, 1, 0]
    
    # Run the simulation
    env = simpy.Environment()
    tipping = set_up_fuzzy_tip(len(shelves_distribution))
    env.process(run_shop(env, num_cashiers, shop_size, products, shelves_distribution, tipping, customers))
    env.run(until=simulation_time)

    return profits_in_time, peolple_at_section, tips_in_time



if __name__ == "__main__":
    size = 100
    cashiers = 20
    time = 10
    main(size, cashiers, time, [])
    print(profits_in_time[-1])
    [print(j) for j in [i for i in peolple_at_section]]



