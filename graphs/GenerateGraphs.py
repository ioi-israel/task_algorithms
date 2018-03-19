"""
Auxiliary functions for generating bipartite and non-bipartite graphs.
"""


import random

from task_algorithms.arrays.Partitions import partition_array


def create_edge(vertex1, vertex2):
    """
    Return an edge between the two vertices.
    The edge is either (v1, v2) or (v2, v1), chosen randomly.
    """
    if random.randint(0, 1) == 0:
        return (vertex1, vertex2)
    return (vertex2, vertex1)


def generate_tree(vertices):
    """
    Generate a list of edges on the given vertices that form a tree.
    """

    n = len(vertices)
    edges = []

    # Choose the parent of each vertex randomly from the previous vertices.
    for i in xrange(1, n):
        vertex = vertices[i]
        parent = vertices[random.randint(0, i - 1)]
        edges += [create_edge(vertex, parent)]
    random.shuffle(edges)
    return edges


def generate_path(vertices):
    """
    Return a list of edges that form a path tree on the given vertices.
    """
    edges = []
    for i in xrange(1, len(vertices)):
        edges += [create_edge(vertices[i - 1], vertices[i])]
    random.shuffle(edges)
    return edges


def generate_component(vertices, num_edges=None, max_edges=None):
    """
    Generate a list of edges on the given vertices,
    that form a connected component.

    If num_edges is given, it is the exact number of edges
    to create. It must be at least n - 1.

    Otherwise, the number of edges is chosen randomly between
    n - 1 and max_edges. The default of max_edges is the
    maximum possible number of edges (n choose 2).
    """

    n = len(vertices)
    if n <= 1:
        return []

    n_choose_2 = n * (n - 1) / 2
    if max_edges is None:
        max_edges = n_choose_2
    else:
        max_edges = min(max_edges, n_choose_2)
        max_edges = max(max_edges, n - 1)

    if num_edges is None:
        num_edges = random.randint(n - 1, max_edges)
    else:
        num_edges = min(num_edges, max_edges)
        num_edges = max(num_edges, n - 1)

    assert num_edges <= 10**7

    # Start with a tree, and add extra edges.
    tree_edges = set(generate_tree(vertices))
    num_other_edges = num_edges - (n - 1)
    other_edges = _generate_random_edges(vertices, tree_edges, num_other_edges)

    edges = list(tree_edges) + other_edges
    random.shuffle(edges)
    return edges


def _contains_edge(edges_set, vertex1, vertex2):
    """
    Check if the container has an edge between the given vertices.
    The edge can be (vertex1, vertex2) or (vertex2, vertex1).
    """
    return (vertex1, vertex2) in edges_set or (vertex2, vertex1) in edges_set


def _generate_random_edges(vertices, pre_existing=None, num_edges=None,
                           max_edges=None):
    """
    Return a list of edges on the given vertices.
    If the total amount of possible edges is small enough,
    it is generated and a random sample is returned.
    Otherwise, edges are randomly added until the resulting
    set is large enough.

    Optionally, pre_existing is a set of edges that
    should not be used and don't count.

    If num_edges is given, it is the exact number of new edges
    to create. Otherwise, it is chosen randomly between 0 and
    max_edges (default for max_edges is the maximum possible).
    """

    n = len(vertices)
    if n <= 1:
        return []

    if pre_existing is None:
        pre_existing = set()

    n_choose_2 = n * (n - 1) / 2
    max_possible = n_choose_2 - len(pre_existing)

    if max_edges is None:
        max_edges = max_possible
    else:
        max_edges = min(max_edges, max_possible)
        max_edges = max(0, max_edges)

    if num_edges is None:
        num_edges = random.randint(0, max_edges)
    else:
        num_edges = min(num_edges, max_edges)
        num_edges = max(0, num_edges)

    if num_edges == 0:
        return []

    edges_set = set()

    # If number of edges is small compared to the possibilities,
    # add edges randomly until the number fits.
    if 2 * num_edges < max_possible:
        while len(edges_set) < num_edges:
            vertex1 = random.choice(vertices)
            vertex2 = random.choice(vertices)
            if vertex1 == vertex2:
                continue
            if _contains_edge(edges_set, vertex1, vertex2):
                continue
            if _contains_edge(pre_existing, vertex1, vertex2):
                continue
            edges_set.add(create_edge(vertex1, vertex2))

    # Otherwise, generate all possibilities and take a sample.
    else:
        assert n <= 10000
        options = []
        for i in xrange(n):
            vertex1 = vertices[i]
            for j in xrange(i + 1, n):
                vertex2 = vertices[j]
                if _contains_edge(pre_existing, vertex1, vertex2):
                    continue
                options += [create_edge(vertex1, vertex2)]
        edges_set.update(random.sample(options, num_edges))

    edges = list(edges_set)
    random.shuffle(edges)
    return edges


def generate_forest(vertices, num_comps=None):
    """
    Return a list of edges between the given vertices,
    such that the graph is a forest.

    The number of components (trees) is num_comps.
    The default is set randomly between 1 and n.
    The component sizes are random.
    """

    n = len(vertices)
    if n <= 1:
        return []

    if num_comps is None:
        num_comps = random.randint(1, n)
    num_comps = min(num_comps, n)
    num_comps = max(num_comps, 1)

    chunks = partition_array(vertices, num_comps)
    edges = []
    for (index1, index2) in chunks:
        component = vertices[index1:index2 + 1]
        edges += generate_tree(component)

    random.shuffle(edges)
    return edges


def generate_graph(vertices, num_edges, connected=False):
    """
    Return a list of edges between the given vertices.
    The number and size of connected component are random.

    If connected is true, the resulting graph is connected.
    Otherwise, there is no guarantee.
    """

    if connected:
        return generate_component(vertices, num_edges)
    return _generate_random_edges(vertices, num_edges=num_edges)


def generate_bipartite_graph(vertices, max_edges=None):
    """
    Return a list of edges between the given vertices,
    such that the resulting graph is bipartite.

    The number of edges is up to max_edges. By default,
    it is chosen randomly between 0 and the number of
    possible edges.

    The size of each side of the graph is chosen randomly
    between 1 and n - 1.
    """

    n = len(vertices)
    if n <= 1:
        return []

    left_size = random.randint(1, n - 1)
    right_size = n - left_size

    left_side = random.sample(vertices, left_size)
    right_side = list(set(vertices) - set(left_side))
    random.shuffle(right_side)

    max_possible = left_size * right_size
    if max_edges is None:
        max_edges = max_possible
    else:
        max_edges = min(max_edges, max_possible)
        max_edges = max(max_edges, 0)

    num_edges = random.randint(0, max_edges)

    edges_set = set()

    # If the number of possibilities is large, choose randomly.
    if 2 * num_edges < max_possible:
        while len(edges_set) < num_edges:
            vertex1 = random.choice(left_side)
            vertex2 = random.choice(right_side)
            if _contains_edge(edges_set, vertex1, vertex2):
                continue
            edges_set.add(create_edge(vertex1, vertex2))

    # Otherwise, generate all possibilities and take a sample.
    else:
        assert max_possible <= 10 ** 7
        options = []
        for vertex1 in left_side:
            for vertex2 in right_side:
                options += [create_edge(vertex1, vertex2)]
        edges_set.update(random.sample(options, num_edges))

    edges = list(edges_set)
    random.shuffle(edges)
    return edges
