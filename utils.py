import collections

def breadth_first_search(graph : list, root : tuple, destination : tuple):
    dir_row = [0, 1, 0, -1]
    dir_col = [1, 0, -1, 0]
    visited, queue, pi = set(), collections.deque([root]), {tuple : tuple}
    while queue: 
        vertex = queue.popleft()
        for i in range(len(dir_row)):
            neighbour = graph[vertex[0] + dir_row[i], vertex[1] + dir_col[i]]
            if neighbour not in visited:
                visited.add(neighbour) 
                queue.append(neighbour)
                pi[neighbour] = vertex
    return road_to_root(pi, destination, [])

def road_to_root(pi: dict, node, road: list):
    if node not in pi.keys:
        return road
    road.append(pi[node])
    road_to_root(pi, pi[node], road)