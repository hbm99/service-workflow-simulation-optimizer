import collections
from environment import Section, Cashier
from walking_problem.heuristic_problem_utils import Problem
from typing import List
from environment import Cell

DIR_ROW = [0, 1, 0, -1, 1, -1, -1, 1]
DIR_COL = [1, 0, -1, 0, 1, 1, -1, -1]

def distance(graph : list, root : tuple, destination : tuple):
    return len(breadth_first_search(graph, root, destination, True))

def distance_no_obstacles(graph : list, root : tuple, destination : tuple):
    return len(breadth_first_search(graph, root, destination, False))

def breadth_first_search(graph : list, root : tuple, destination : tuple, obstacled : bool = True):
    
    visited, queue, pi = set(), collections.deque([root]), {tuple : tuple}
    while queue:
        vertex = queue.popleft()
        # vertex_position = vertex.position
        # if vertex != None:
        #     vertex_pos = vertex.pos
        for i in range(len(DIR_ROW)):
            if not is_inside(graph, vertex[0] + DIR_ROW[i], vertex[1] + DIR_COL[i]):
                continue
            
            neighbour = graph[vertex[0] + DIR_ROW[i]][vertex[1] + DIR_COL[i]]
            
            if obstacled and is_obstacle(neighbour):
                continue
            
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour.position)
                pi[neighbour.position] = vertex
    
    return road_to_root(pi, destination, [])

def is_obstacle(object):
    return isinstance(object, Section) or isinstance(object, Cashier)


def road_to_root(pi: dict, node, road: list):
    if node not in pi.keys():
        return road
    road.append(pi[node])
    road_to_root(pi, pi[node], road)

def is_inside(map, x, y):
    is_inside = x >= 0 and y >= 0 and x < len(map) and y < len(map[0])
    return is_inside

class WalkingProblem(Problem):
    """Shop's walking problem."""
    
    def h(self, node):
        return distance_no_obstacles(self.shop_map, self.initial, self.goal[0]) #picking as goal the first item to buy from shopping list for heuristic, pending to change in next versions and set it with closer item to client 
    
    def actions(self, state : List[int]):
        """The actions executable in this state."""
        x0, y0 = state
        actions = []
        for i in range(len(DIR_ROW)):
            if is_inside(self.shop_map, x0 + DIR_ROW[i], y0 + DIR_COL[i]):
                actions.append(('Move', (x0, y0), (x0 + DIR_ROW[i], y0 + DIR_COL[i])))
        
        # ([('Move', (x0, y0), (x0 + DIR_ROW[i], y0 + DIR_COL[i])) for i in range(len(DIR_ROW)) if is_inside(self.shop_map, x0 + DIR_ROW[i], y0 + DIR_COL[i])])
        return actions

    def result(self, state, action):
        """The state that results from executing this action in this state."""
        act, (x0, y0), (x1, y1) = action
        if act == 'Move':
            result = (x1, y1)
            self.places.append(result)
        return result

    def is_goal(self, state):
        """True if person went through every shopping list item."""
        return self.goal in self.places