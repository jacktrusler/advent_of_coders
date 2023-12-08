from typing import Iterable


def pairwise(iterable: Iterable):
    a = iter(iterable)
    return zip(a, a)