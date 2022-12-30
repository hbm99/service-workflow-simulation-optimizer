def is_inside(map, x, y):
    return x >= 0 and y >= 0 and x < len(map) and y < len(map[0])

def is_obstacle(cell):
    return False

def take_adj_list(map, a):
    adj = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == dc == 0:
                continue
            step = (a[0]+dr, a[1]+dc)
            if is_inside(map, step[0], step[1]):
                   adj.append(step)
    #print(adj)
    return adj

def recursive_dfs(map, root, goal: str) -> list:
    """
    Return the depth first search path from root to gaol.
    
    Args:
        root: the starting node for the search
        goal: the goal node for the search
        
    Returns: a list with the path from root to goal
    
    Raises: ValueError if goal isn't in the graph
    """
    path = _dfs(map, [root], goal, dict())
    if path is None:
        raise ValueError('goal not in graph')
    return path

def _dfs(map, path: list, goal: str, visited: dict) -> list:
    """
    Perform a Depth First Search step.
    
    Args:
        path: the current path of nodes
        goal: the goal node label
        visited: the dictionary of visited nodes
    """
    current = path[-1]
    # if this is the goal, return the path
    if current == goal:
        print(path)
        return path
    # visit this node
    visited[current] = True
    # generate a list of unvisited children and iterate over it
    neighborhood = take_adj_list(map, current)

    unvisited = [child for child in neighborhood if child not in visited]
    for child in unvisited:
        # generate a new path and recursively call
        new_path = list(path)
        new_path.append(child)
        sub_path = _dfs(map, new_path, goal, visited)
        # make sure the sub path is valid before returning
        if sub_path is not None:
            return sub_path
        else:
            continue
    # the search couldn't find the goal
    return None

def dfs_recursive(graph, source, goal, path = []):  
    print(path)
    if goal == source:
        print(goal)
        print("wi")
        print(source)
        path.append(goal)
        return path

    if source not in path:  
        new_path = list(path)
        new_path.append(source) 

        if not is_inside(graph, source[0], source[1]):
               # leaf node, backtrack  
            return path  
        neighborhood = take_adj_list(map, source)
        for neighbour in  neighborhood:

            sub_path = dfs_recursive(graph, neighbour, goal, new_path)
        # make sure the sub path is valid before returning
            if sub_path is not None:
                return sub_path
            else:
                continue
  
            #path = dfs_recursive(graph, neighbour, goal, path)  
  
  
    return path

map = [[1, 2, 3, 7 , 9], [1, 2, 3, 7 , 9], [1, 2, 3, 7 , 9], [1, 2, 3, 7 , 9], [1, 2, 3, 7 , 9]]
p = recursive_dfs(map, (0,0), (4,3))
#print(p)