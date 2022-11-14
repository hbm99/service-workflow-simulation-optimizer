import random

from customer import Customer
from environment import ShopEnvironment


def main():

    # Setting up the environment 
    sections_name = ["food","cleaning","toiletries", "household_items"]
    shop_environment= ShopEnvironment(sections_name, number_of_cashiers=2)

    ammount_of_clients= 100
    customers_list=[]

   # Pendiente Tener en cuenta ordenar a clientes por arrival_time
   #Pendiente annadir personalidad del cliente
    for i in range(ammount_of_clients):
        arrival_time= 0 #exponential_distribution
        shopping_list= fill_shopping_list(shop_environment)
        customers_list.append(Customer(arrival_time, shopping_list,
                                        shop_environment))


def fill_shopping_list(shop_environment):
    shopping_list = {}
    len_shopping_list= random.randint(0,len(shop_environment))
    possible_indexes= [i for i in range(len(shop_environment.sections))]

    for i in range (len_shopping_list):
        index= random.choice(possible_indexes)
        possible_indexes.pop(index)
        shopping_list[shop_environment.sections[index]]=1 
    
    return shopping_list
        



