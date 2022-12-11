import collections
from environment import Section, Cashier
from heuristic_problem_utils import Problem
from typing import List

DIR_ROW = [0, 1, 0, -1, 1, -1, -1, 1]
DIR_COL = [1, 0, -1, 0, 1, 1, -1, -1]

def distance(graph : list, root: tuple, destination : tuple):
    return len(breadth_first_search(graph, root, destination, True))

def distance_no_obstacles(graph : list, root: tuple, destination : tuple):
    return len(breadth_first_search(graph, root, destination, False))

def breadth_first_search(graph : list, root : tuple, destination : tuple, obstacled : bool = True):
    
    visited, queue, pi = set(), collections.deque([root]), {tuple : tuple}
    while queue:
        vertex = queue.popleft()
        for i in range(len(DIR_ROW)):
            neighbour = graph[vertex[0] + DIR_ROW[i], vertex[1] + DIR_COL[i]]
            if obstacled and is_obstacle(neighbour): 
                continue
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
                pi[neighbour] = vertex
    return road_to_root(pi, destination, [])

def is_obstacle(object):
    return isinstance(object, Section) or isinstance(object, Cashier)


def road_to_root(pi: dict, node, road: list):
    if node not in pi.keys:
        return road
    road.append(pi[node])
    road_to_root(pi, pi[node], road)

class WalkingProblem(Problem):
    """Problem about walking to buying items at a shop."""
    
    def actions(self, state : List[int, int]):
        """The actions executable in this state."""
        x0, y0 = state
        return ([('Move', (x0, y0), (x0 + DIR_ROW[i], y0 + DIR_COL[i])) for i in range(len(DIR_ROW)) if is_inside(x0 + DIR_ROW[i], y0 + DIR_COL[i])])

    def result(self, state, action):
        """The state that results from executing this action in this state."""
        act, (x0, y0), (x1, y1) = action
        if act == 'Move':
            result = (x1, y1)
        return result

    def is_goal(self, state):
        """True if person went through every shopping list item."""
        # pending
        pass