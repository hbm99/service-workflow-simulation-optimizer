from walking_problem.heuristic_problem_utils import astar_search, path_actions, path_states
from walking_problem.walking_problem_utils import WalkingProblem
from environment import ShopEnviroment, Cell

shop_environment = ShopEnviroment(8, ["A"], 1)

p = WalkingProblem((0, 0), [(0, 1), (1, 3)], places = [], shop_map = shop_environment.map)

sol = astar_search(p)
print(path_actions(sol))
print(path_states(sol))