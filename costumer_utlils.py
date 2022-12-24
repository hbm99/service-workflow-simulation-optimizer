################### Auxiliar methods for Go with dfs #############################################
    
def Valid_pos(map, step) -> bool:
    try:
        map[step[0]], [step[1]]
    except:
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

def dfs(self, map, start, target, path = [], visited = set()):
    path.append(start)
    visited.add(start)
    if start == target:
        return path
    for neighbour in self.Take_adj_list(map, start):
        if neighbour not in visited:
            result = self.dfs(neighbour, target, path, visited)
            if result is not None:
                return result
    path.pop()
    return None