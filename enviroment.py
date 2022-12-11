from joblib import Parallel


class ShopEnviroment:
    def __init__(self, sections_names, server_count):
        # list of the sections that split the shop
        self.sections = {}
        for name in sections_names:
            self.sections[name] = Section(name)

        # list of cashiers at the shop
        self.cashier = [ParallelServer() for i in range(server_count)]

class Section:
    def __init__(self, name):
        self.name = name
        self.client_count = 0

class ParallelServer():
    pass
