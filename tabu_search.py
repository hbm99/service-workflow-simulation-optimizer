import random as rd
from itertools import combinations

from simpy import rt

from fuzzy_logic import set_up_fuzzy_tip
from simulation import profits_in_time, run_shop


class TabuSearch():
    def __init__(self, shelf_count, products, shop_size, num_cashier, simulation_time, max_iter,  tabu_tenure = 2):
        
        #Tabu Tenure: This defines the size of the Tabu list, i.e., for how many 
        # iterations a solution component is kept as Tabu
        self.max_iter= max_iter
        self.tabu_tenure = tabu_tenure
        self.Penalization_weight = 3
        


        # Simulation arguments
        self.shelf_count= shelf_count
        self.products= products
        self.shop_size= shop_size
        self.num_cashier= num_cashier
        self.sim_time= simulation_time
        self.products_dict = {item.name : item for item in self.products}

        

        self.Initial_solution = self.get_InitialSolution()

        self.tabu_str, self.Best_solution, self.Best_objvalue = self.TSearch(max_iter)


    def get_tabuestructure(self):
        '''Takes a dict (input data)
        Returns a dict of tabu attributes(pair of jobs that are swapped) as keys and [tabu_time, MoveValue,
        frequency count, penalized MoveValue]
        '''
        dict = {}
        for swap in combinations(range(self.shelf_count), 2):
            dict[swap] = {'tabu_time': 0, 'MoveValue': 0, 'freq': 0, 'Penalized_MV': 0}
        return dict

    def get_InitialSolution(self, show=False):
     
        initial_solution = list(range(self.shelf_count))

        # Filling shelves with random products
        for i in range(len(initial_solution)):
            initial_solution[i]= self.products.index(rd.choice(self.products))

        #rd.seed(self.seed)
        #rd.shuffle(initial_solution)

        if show == True:
            print("initial Random Solution: {}".format(initial_solution))
        return initial_solution


    def fitness(self,solution):
        ''' This method must initialize the simulation and run it to get the profits 
        with the current shelves organization. The return value must be -(profits)'''
        
        # Run the simulation
        print(f"Starting simulation. Distribution: {solution}")
        env = rt.RealtimeEnvironment(factor=0.001, strict=False)
        tipping = set_up_fuzzy_tip(len(solution))
        env.process(run_shop(env, self.num_cashier, self.shop_size, self.products_dict, solution, tipping))
        env.run(until=self.sim_time)
        profits= profits_in_time[-1]
        print(f"Got ${str(profits)} at {solution}")
        return -profits

    def SwapMove(self, solution, i ,j):
        '''Takes a list (solution)
        returns a new neighbor solution with i, j swapped
       '''
        solution = solution.copy()
        #Swap
        solution[i], solution[j] = solution[j], solution[i]
        return solution

    def MutationMove(self,solution):
        new_sol= solution.copy()
        products_indices= [i for i in range(len(self.products))]
        not_allocated_prod = list(set(products_indices) - set(solution))
        section_to_mutate= rd.randint(0, len(solution)-1)
        new_product= rd.choice(not_allocated_prod)
        new_sol[section_to_mutate]= new_product
        return solution



    def TSearch(self, max_iter):
        '''The implementation Tabu search algorithm with long-term memory and pair_swap as Tabu attribute with
        diversification.
        '''
        # Parameters:
        tenure =self.tabu_tenure
        tabu_structure = self.get_tabuestructure()  # Initialize the data structures
        
        best_solution = self.Initial_solution
        best_objvalue = self.fitness(best_solution)
        
        current_solution = self.Initial_solution
        current_objvalue = best_objvalue

        print("#"*30, "TS with Tabu Tenure: {}\nInitial Solution: {}, Initial Objvalue: {}".format(
            tenure, current_solution, -current_objvalue), "#"*30, sep='\n\n')

        iter = 1
        Terminate = 0
    
        while iter < max_iter: #Terminate < max_iter:

            print('\n\n### iter {}###  Current_Objvalue: {}, Best_Objvalue: {}'.format(iter, -current_objvalue,
                                                                                    -best_objvalue))
            
            # Searching the whole neighborhood of the current solution:
            for move in tabu_structure.keys():
                candidate_solution = self.SwapMove(current_solution, move[0], move[1])
                #mutation= rd.random()
                #if(mutation>0.75): candidate_solution = self.MutationMove(current_solution)
                candidate_objvalue = self.fitness(candidate_solution)
                tabu_structure[move]['MoveValue'] = candidate_objvalue
                # Penalized objValue by simply adding freq to Objvalue (minimization):
                tabu_structure[move]['Penalized_MV'] = candidate_objvalue + (tabu_structure[move]['freq'] *
                                                                             self.Penalization_weight)

            # Admissible move
            while True:
                # select the move with the lowest Penalized ObjValue in the neighborhood (minimization)
                best_move = min(tabu_structure, key =lambda x: tabu_structure[x]['Penalized_MV'])
                MoveValue = tabu_structure[best_move]["MoveValue"]
                tabu_time = tabu_structure[best_move]["tabu_time"]
                # Penalized_MV = tabu_structure[best_move]["Penalized_MV"]
                # Not Tabu
                if tabu_time < iter:
                    # make the move
                    current_solution = self.SwapMove(current_solution, best_move[0], best_move[1])
                    current_objvalue = MoveValue #self.Objfun(current_solution)
                    # Best Improving move
                    if MoveValue < best_objvalue:
                        best_solution = current_solution
                        best_objvalue = current_objvalue
                        print("   best_move: {}, Objvalue: {} => Best Improving => Admissible".format(best_move,
                                                                                                      -current_objvalue))
                        Terminate = 0
                    else:
                        print("   ##Termination: {}## best_move: {}, Objvalue: {} => Least non-improving => "
                              "Admissible".format(Terminate,best_move,
                                                                                                          - current_objvalue))
                        Terminate += 1
                    # update tabu_time for the move and freq count
                    tabu_structure[best_move]['tabu_time'] = iter + tenure
                    tabu_structure[best_move]['freq'] += 1
                    iter += 1
                    break
                # If tabu
                else:
                    # Aspiration
                    if MoveValue < best_objvalue:
                        # make the move
                        current_solution = self.SwapMove(current_solution, best_move[0], best_move[1])
                        current_objvalue = MoveValue

                        best_solution = current_solution
                        best_objvalue = current_objvalue
                        print("   best_move: {}, Objvalue: {} => Aspiration => Admissible".format(best_move,
                                                                                                      -current_objvalue))
                        tabu_structure[best_move]['freq'] += 1
                        Terminate = 0
                        iter += 1
                        break
                    else:
                        tabu_structure[best_move]['Penalized_MV'] = float('inf')
                        print("   best_move: {}, Objvalue: {} => Tabu => Inadmissible".format(best_move,
                                                                                              -current_objvalue))
                        continue
        print('#'*50 , "Performed iterations: {}".format(iter), "Best found Solution: {} , Objvalue: {}".format(best_solution,-best_objvalue), sep="\n")
        return tabu_structure, best_solution, -best_objvalue


