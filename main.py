from walking_problem.heuristic_problem_utils import astar_search, path_actions, path_states
from walking_problem.walking_problem_utils import WalkingProblem

p = WalkingProblem([(0, 0)], [(0, 1), (1, 3)], places = [])

sol = astar_search(p)
path_actions(sol), path_states(sol)