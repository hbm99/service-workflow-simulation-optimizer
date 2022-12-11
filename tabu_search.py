
'''PSEUDOCODIGO
     1 sBest ← s0
     2 bestCandidate ← s0
     3 tabuList ← []
     4 tabuList.push(s0)
     5 while (not stoppingCondition())
     6 	sNeighborhood ← getNeighbors(bestCandidate)
     7 	bestCandidate ← sNeighborHood.firstElement
     8 	for (sCandidate in sNeighborHood)
     9 		if ( (not tabuList.contains(sCandidate)) and (fitness(sCandidate) > fitness(bestCandidate)) )
    10 			bestCandidate ← sCandidate
    11 		end
    12 	end
    13 	if (fitness(bestCandidate) > fitness(sBest))
    14 		sBest ← bestCandidate
    15 	end
    16 	tabuList.push(bestCandidate)
    17 	if (tabuList.size > maxTabuSize)
    18 		tabuList.removeFirst()
    19 	end
    20 end
    21 return sBest
    
    '''

class  Tabu_Search:

    def __init__(self, initial_solution, max_iter, tabu_list_max_size=10) -> None:
        self.initial_solution = initial_solution
        self.elite_candidate = [initial_solution]
        self.max_iter = max_iter
        self.tabu_list_max_size = tabu_list_max_size

    def execute(self):
        i=0
        best_sol= self.initial_solution
        best_candidate= self.initial_solution
        tabu_list=[]
        while (i < self.max_iter):

            s_neighbors = self.find_neighbors(best_candidate) 
            best_candidate= s_neighbors.first_element
            for s_candidate in s_neighbors:
                if not tabu_list.__contains__(s_candidate) and self.fitness(s_candidate> self.fitness(best_candidate)):
                    best_candidate = s_candidate

            if self.fitness(best_candidate) > self.fitness(best_sol):
                 best_sol = best_candidate
            tabu_list.append(best_candidate)

            if len(tabu_list) > self.tabu_list_max_len:
                tabu_list.remove(tabu_list[0])

            #for item in self.elite_candidate:
                
    def fitness(self):
        pass

    def find_neighbors(self):
        pass








