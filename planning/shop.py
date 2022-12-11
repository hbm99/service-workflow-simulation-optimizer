from planning.planning import Action , PlanningProblem
from planning.planning import ForwardPlan
from planning.search import *
from planning.planning import Action
from enviroment import Section, ShopEnviroment

def shop_problem(client, enviroment):

    sections = enviroment.sections
    #shopping_list = client.get_shopping_list()
    shopping_list = ['Fruta', 'vegetal']
    initial = "ClientAt(entry)"
    goals = "ClientAt(exit)"
    domainn = "Section(entry) & Section(exit)"
    #for section in client.get_shopping_list().keys():
    for section in shopping_list:
       # goals += f" & ClientBought({section.name})"
        goals += f" & ClientBought({section})"

    for section in enviroment.sections.keys():
       # initial += f" & ProductoEn({section.name}p, {section.name})"
        initial += f" & ProductoEn({section}p, {section})"
       # domainn += f" & Section({section.name})"
        domainn += f" & Section({section})"
        #domainn += f" & Product({section.name}p)"
        domainn += f" & Product({section}p)"


    return PlanningProblem(initial=initial, 
                           goals=goals,
                           actions=[Action('Go(A, B)',
                                           precond='ClientAt(A)',
                                           effect='~ClientAt(A) & ClientAt(B)',
                                           domain='Section(A) & Section(B)'),
                                    Action('Buy(p, C)',
                                           precond='ClientAt(C) & ClientGet(p) & ProductAt(p, C)',
                                           effect='ClientBought(p)',
                                           domain='Section(C) & Product(p)'),
                                    Action('Take(p, A)',
                                           precond='ClienAt(A) & ProductAt(p, A)',
                                           effect='ClientGet(p)',
                                           domain='Section(A) & Product(p)'),],
                           domain=domainn)
e = ShopEnviroment(['vegetal', 'cerveza', 'fruta'], 8)
pp = shop_problem(2, e)

variables ,problem = shop_problem(2,e)
sol = breadth_first_tree_search(ForwardPlan(problem))
print(sol)
