import simpy
from environment import Product
from simulation import run_shop, profits_in_time
from fuzzy_logic import set_up_fuzzy_tip
from tabu_search import TabuSearch


def main():
    # Shop parameters
    shop_size = 10
    num_cashiers = 2
    list_product = [Product('PIZZA', 10), Product('PAN', 5), Product('TOMATE', 3), Product('LECHUGA', 1), Product('JUGUETE', 20), Product('CERVEZA', 3), Product('CHOCOLATE', 2)]
    simulation_time = 60 * 60
    shelves_count= 4
    
    #Optimization parameters
    opt_max_iter= 6

    # Simulation results parameters
    sim_numb= 1
    results= []

    for _ in range(sim_numb):
        ts= TabuSearch(shelves_count, list_product,shop_size, num_cashiers, simulation_time, opt_max_iter)
        results.append((ts.Best_solution, ts.Best_objvalue))
    
    print (results)


if __name__ == "__main__":
    main()



