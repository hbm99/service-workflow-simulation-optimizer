################### Auxiliar methods for Go with dfs #############################################
    
from sympy import true


def Valid_pos(map, step) -> bool:
    if(step[0] < 0 or step[1] < 0):
        return False
    if(step[0] > len(map[0]) or step[1] > len(map)):
        return False
    return True

def Take_adj_list(map, a):
    adj = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == dc == 0:
                continue
            step = (a[0]+dr, a[1]+dc)
            if Valid_pos(map, step):
                   adj.append(step)
    return adj

def dfs(map, start, target, path = [], visited = set()):
    path.append(start)
    visited.add(start)
    if start == target:
        return path
    neighborhood = Take_adj_list(map, start)
    for neighbour in  neighborhood:
        if neighbour not in visited:
            result = dfs(map, neighbour, target, path, visited)
            if result is not None:
                return result
    path.pop()
    return None