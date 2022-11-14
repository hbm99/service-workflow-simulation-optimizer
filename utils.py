import collections

def breadth_first_search(graph : list, root : tuple): 
    visited, queue = set(), collections.deque([root])
    while queue: 
        vertex = queue.popleft()
        for neighbour in graph[vertex]: # pending defining neighbours as 4 possibble movements (with direction arrays, etc)
            if neighbour not in visited: 
                visited.add(neighbour) 
                queue.append(neighbour) 