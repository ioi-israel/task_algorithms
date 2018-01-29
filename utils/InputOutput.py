"""
Utilities for generating input and output strings.
"""


def seq_to_str(seq, sep="\n", with_len=True, len_sep="\n", end_sep="\n"):
    """
    Convert a Python sequence into a string with the given separator.
    Each item is converted to a string using str().
    If with_len is given, put the length first, and separate it from the
    rest with len_sep. Finish with end_sep.
    """
    result = ""
    if with_len:
        result += "%d%s" % (len(seq), len_sep)
    result += sep.join(str(i) for i in seq) + end_sep
    return result
