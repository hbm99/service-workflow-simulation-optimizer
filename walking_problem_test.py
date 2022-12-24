from walking_problem.heuristic_problem_utils import astar_search, path_actions, path_states
from walking_problem.walking_problem_utils import WalkingProblem
from environment import Cell

map = [[None] * 10] * 10
for i in range(len(map)):
    for j in range(len(map[0])):
        map[i][j] = Cell((i, j))

start = (0, 0)
for item_to_buy in [(5, 5), (2, 3)]:
    p = WalkingProblem(start, [item_to_buy], shop_map = map)

    sol = astar_search(p)
    print(path_actions(sol))
    print(path_states(sol))
    
    start = item_to_buy