import random as rd
from itertools import combinations
import math

class TabuSearch():
    def __init__(self, shelf_count, products, max_iter,  tabu_tenure = 2):
        
        #Tabu Tenure: This defines the size of the Tabu list, i.e., for how many 
        # iterations a solution component is kept as Tabu
        self.tabu_tenure = tabu_tenure



        self.shelf_count= shelf_count

        #self.shelves= {}
        #for i in range(self.shelf_count):
        #  self.shelves[i]= []

        self.products= products

        self.Penalization_weight = 3

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
            initial_solution[i]= rd.choice(self.products)

        #rd.seed(self.seed)
        #rd.shuffle(initial_solution)

        if show == True:
            print("initial Random Solution: {}".format(initial_solution))
        return initial_solution


    def fitness(self,solution):
        ''' This method must initialize the simulation and run it to get the profits 
        with the current shelves organization. The return value must be -(profits)'''
        return 0

    def Objfun(self, solution, show = False):
        '''Takes a set of scheduled jobs, dict (input data)
        Return the objective function value of the solution
        '''
        dict = self.instance_dict
        t = 0   #starting time
        objfun_value = 0
        for job in solution:
            C_i = t + dict[job]["processing_time"]  # Completion time
            d_i = dict[job]["due_date"]   # due date of the job
            T_i = max(0, C_i - d_i)    #tardiness for the job
            W_i = dict[job]["weight"]  # job's weight

            objfun_value +=  W_i * T_i
            t = C_i
        if show == True:
            print("\n","#"*8, "The Objective function value for {} solution schedule is: {}".format(solution ,objfun_value),"#"*8)
        return objfun_value

    def SwapMove(self, solution, i ,j):
        '''Takes a list (solution)
        returns a new neighbor solution with i, j swapped
       '''
        solution = solution.copy()
        #Swap
        solution[i], solution[j] = solution[j], solution[i]
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

        print("#"*30, "Short-term memory TS with Tabu Tenure: {}\nInitial Solution: {}, Initial Objvalue: {}".format(
            tenure, current_solution, current_objvalue), "#"*30, sep='\n\n')

        iter = 1
        Terminate = 0
    
        while iter < max_iter: #Terminate < max_iter:

            print('\n\n### iter {}###  Current_Objvalue: {}, Best_Objvalue: {}'.format(iter, current_objvalue,
                                                                                    best_objvalue))
            
            # Searching the whole neighborhood of the current solution:
            for move in tabu_structure.keys():
                candidate_solution = self.SwapMove(current_solution, move[0], move[1])
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
                                                                                                      current_objvalue))
                        Terminate = 0
                    else:
                        print("   ##Termination: {}## best_move: {}, Objvalue: {} => Least non-improving => "
                              "Admissible".format(Terminate,best_move,
                                                                                                           current_objvalue))
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
                                                                                                      current_objvalue))
                        tabu_structure[best_move]['freq'] += 1
                        Terminate = 0
                        iter += 1
                        break
                    else:
                        tabu_structure[best_move]['Penalized_MV'] = float('inf')
                        print("   best_move: {}, Objvalue: {} => Tabu => Inadmissible".format(best_move,
                                                                                              current_objvalue))
                        continue
        print('#'*50 , "Performed iterations: {}".format(iter), "Best found Solution: {} , Objvalue: {}".format(best_solution,best_objvalue), sep="\n")
        return tabu_structure, best_solution, best_objvalue


