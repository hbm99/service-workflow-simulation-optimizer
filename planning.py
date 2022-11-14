from enviroment import Section, ShopEnviroment

def shop_problem(client, enviroment):

    sections = enviroment.sections
    shopping_list = client.get_shopping_list()
    initial = "ClientAt(entry)"
    goals = "ClientAt(exit)"
    domainn = "Section(entry) & Section(exit)"
    for section in client.get_shopping_list().keys():
        goals += f" & ClientBought({section.name})"

    for section in enviroment.sections.keys():
        initial += f" & ProductoEn({section.name}p, {section.name})"
        domainn += f" & Section({section.name})"
        domainn += f" & Product({section.name}p)"


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