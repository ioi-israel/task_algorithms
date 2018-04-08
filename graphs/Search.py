"""
Graph search algorithms.
"""


from collections import defaultdict


def get_components(vertices, edges):
    """
    Get a list of connected components in the graph.
    Each component is a list of vertices.
    """
    neighbors = defaultdict(set)
    for (u, v) in edges:
        neighbors[u].add(v)
        neighbors[v].add(u)

    visited = set()

    def dfs(v, comp):
        """
        Perform DFS from v, and fill the component set.
        """

        stack = [v]
        while stack:
            u = stack.pop()
            if u in visited:
                continue
            visited.add(u)
            comp.add(u)
            stack += list(neighbors[u])

    comps = []
    for v in vertices:
        comp = set()
        dfs(v, comp)
        if comp:
            comps += [list(comp)]
    return comps
