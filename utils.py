import collections
from environment import Section, Cashier

def distance(graph : list, root: tuple, destination : tuple):
    return len(breadth_first_search(graph, root, destination, True))

def distance_no_obstacles(graph : list, root: tuple, destination : tuple):
    return len(breadth_first_search(graph, root, destination, False))

def breadth_first_search(graph : list, root : tuple, destination : tuple, obstacled : bool = True):
    dir_row = [0, 1, 0, -1, 1, -1, -1, 1]
    dir_col = [1, 0, -1, 0, 1, 1, -1, -1]
    visited, queue, pi = set(), collections.deque([root]), {tuple : tuple}
    while queue:
        vertex = queue.popleft()
        for i in range(len(dir_row)):
            neighbour = graph[vertex[0] + dir_row[i], vertex[1] + dir_col[i]]
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