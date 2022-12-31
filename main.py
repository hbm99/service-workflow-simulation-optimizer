import simpy
from environment import Product
from simulation import run_shop, profits_in_time
from fuzzy_logic import set_up_fuzzy_tip
from tabu_search import TabuSearch


def main():
    shop_size = 100
    num_cashiers = 20
    list_product = [Product('PIZZA', 10), Product('PAN', 5), Product('TOMATE', 3), Product('LECHUGA', 1), Product('JUGUETE', 20), Product('CERVEZA', 3), Product('CHOCOLATE', 2)]
    products = {item.name : item for item in list_product}
    simulation_time = 60 * 60
    shelves_count= 4

    ts= TabuSearch(shelves_count, list_product,shop_size, num_cashiers, simulation_time, 5)


if __name__ == "__main__":
    main()



