from tabu_search import TabuSearch
from environment import Product

def main(size, cashiers, time, shelves, iterations, sim_n):
    # Shop parameters
    shop_size = size
    num_cashiers = cashiers
    list_product = [Product('PIZZA', 10), Product('PAN', 5), Product('TOMATE', 3), Product('LECHUGA', 1), Product('JUGUETE', 20), Product('CERVEZA', 3), Product('CHOCOLATE', 2)]
    simulation_time = time
    shelves_count= shelves
    
    #Optimization parameters
    opt_max_iter= iterations

    # Simulation results parameters
    sim_numb= sim_n
    results= []
    solutions_fit = []

    for _ in range(sim_numb):
        ts= TabuSearch(shelves_count, list_product,shop_size, num_cashiers, simulation_time, opt_max_iter)
        results.append((ts.Best_solution, ts.Best_objvalue))
        solutions_fit.append(ts.solutions_fit)
    
    print (results)
    return results, solutions_fit


if __name__ == "__main__":
    main(10, 2, 60 * 60, 4, 6, 1)



