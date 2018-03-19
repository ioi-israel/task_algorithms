"""
Functions relating to partitioning arrays.
"""


import random


def partition_array(array, num_chunks):
    """
    Return a sorted list of pairs of indices. Each pair (start, end)
    describes a distinct chunk of the array. Indices are inclusive.
    The union of all chunks is the entire array.
    """

    n = len(array)
    if num_chunks == 0 or num_chunks > n:
        return []

    # We choose only (num_chunks - 1) indices from [0, ... ,n - 2],
    # then add n - 1. Each index is the inclusive end of a chunk.
    indices = sorted(random.sample(xrange(n - 1), num_chunks - 1)) + [n - 1]

    result = [(0, indices[0])]
    for i in xrange(1, len(indices)):
        result += [(indices[i - 1] + 1, indices[i])]
    return result
