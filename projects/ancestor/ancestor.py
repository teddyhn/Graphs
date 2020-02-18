
def earliest_ancestor(ancestors, starting_node, visited=None):
    if visited is None:
        visited = []

    for k in ancestors:
        if k[1] == starting_node:
            visited.append(k[0])
            return earliest_ancestor(ancestors, k[0], visited)
    
    for k in ancestors:
        if k[0] == starting_node and k[0] in visited:
            return k[0]

    return -1
