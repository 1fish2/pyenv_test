"""
sum.pyx -- Cython test code for a `pip install` problem.
"""

import numpy as np
cimport numpy as np
cimport cython

def sum(long[:] input):
    cdef long i, total = 0
    cdef long max = input.shape[0]
    for i in xrange(max):
        total += input[i]
    return total
