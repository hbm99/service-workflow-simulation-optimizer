import collections
import math
from environment import Section, Cashier
from walking_problem.heuristic_problem_utils import Problem

DIR_ROW = [0, 1, 0, -1, 1, -1, -1, 1]
DIR_COL = [1, 0, -1, 0, 1, 1, -1, -1]

def distance(graph : list, root : tuple, destination : tuple):
    return len(breadth_first_search(graph, root, destination, True))

def distance_no_obstacles(graph : list, root : tuple, destination : tuple):
    distance_no_obstacles = math.sqrt((root[0] - destination[0]) ** 2 + (root[1] - destination[1]) ** 2)
    # length = breadth_first_search(graph, root, destination, False)
    return int(distance_no_obstacles)

def breadth_first_search(graph : list, root : tuple, destination : tuple, obstacled : bool = True):
    
    visited, queue, pi = set(), collections.deque([root]), {tuple : tuple}
    visited.add(root)
    while queue:
        vertex = queue.popleft()
        # vertex_position = vertex.position
        # if vertex != None:
        #     vertex_pos = vertex.pos
        for i in range(len(DIR_ROW)):
            
            if not is_inside(graph, vertex[0] + DIR_ROW[i], vertex[1] + DIR_COL[i]):
                continue
            
            neighbour = (vertex[0] + DIR_ROW[i], vertex[1] + DIR_COL[i])
            
            if obstacled and is_obstacle(neighbour):
                continue
            
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
                pi[neighbour] = vertex
    
    return road_to_root(pi, destination, [])


def is_obstacle(cell):
    return isinstance(cell, Section) or isinstance(cell, Cashier)



def road_to_root(pi: dict, node, road: list):
    if node not in pi.keys():
        return len(road)
    road.append(pi[node])
    return road_to_root(pi, pi[node], road)

def is_inside(map, x, y):
    return x >= 0 and y >= 0 and x < len(map) and y < len(map[0])


def take_adj_list(map, a):
    adj = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == dc == 0:
                continue
            step = (a[0]+dr, a[1]+dc)
            if is_inside(map, step[0], step[1]):
                   adj.append(step)
    return adj

def depth_first_search(map, start, target, path = [], visited = set()):
    path.append(start)
    visited.add(start)
    if start == target:
        return path
    neighborhood = take_adj_list(map, start)
    for neighbour in  neighborhood:
        if neighbour not in visited:
            if is_obstacle(neighbour):
                continue
            result = depth_first_search(map, neighbour, target, path, visited)
            if result is not None:
                return result
    path.pop()
    return None

class WalkingProblem(Problem):
    """Shop's walking problem."""
    
    def h(self, node):
        result = distance_no_obstacles(self.shop_map, node.state, self.goal[0])
        return result # picking as goal the first item to buy from shopping list for heuristic, pending to change in next versions and set it with closer item to client 
    
    def actions(self, state):
        """The actions executable in this state."""
        x0, y0 = state
        actions = []
        for i in range(len(DIR_ROW)):
            new_X_place = x0 + DIR_ROW[i]
            new_Y_place = y0 + DIR_COL[i]
            if is_inside(self.shop_map, new_X_place, new_Y_place) and not isinstance(self.shop_map[new_X_place][new_Y_place], Section):
                actions.append(('Move', (x0, y0), (x0 + DIR_ROW[i], y0 + DIR_COL[i])))
        
        # ([('Move', (x0, y0), (x0 + DIR_ROW[i], y0 + DIR_COL[i])) for i in range(len(DIR_ROW)) if is_inside(self.shop_map, x0 + DIR_ROW[i], y0 + DIR_COL[i])])
        return actions

    def result(self, state, action):
        """The state that results from executing this action in this state."""
        act, (x0, y0), (x1, y1) = action
        if act == 'Move':
            result = (x1, y1)
        return result

    def is_goal(self, state):
        """True if person went through every shopping list item."""
        
        # self.places.append(state)
        visited_goals : bool = state in self.goal
        
        # for item in self.goal:
        #     if item not in self.places:
        #         visited_goals = False
        #         break
        
        # new_goal = self.goal
        # for item in self.places:
        #     if item in self.goal:
        #         new_goal = []
        #         for place in self.goal:
        #             if item != place:
        #                 new_goal.append(place)
        # self.goal = new_goal
        
        return visited_goals