#!/usr/bin/env python3
import functools
import numpy
import itertools
import math
import operator
import sympy

def perm(n):
    indices = list(range(n))
    cycles = list(range(n, 0, -1))
    c = 0
    yield c,tuple(indices)
    while n:
        for i in reversed(range(n)):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i+1:] + indices[i:i+1]
                cycles[i] = n - i
                if i < (n-1):
                    c += 1
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                if i != n-j:
                    c += 1
                yield 1-c%2*2,tuple(indices)
                break
        else:
            return

def determinant(X):
    m,n = numpy.shape(X)
    assert m==n
    return sum(s * functools.reduce(operator.mul, (X[p[i],i] for i in range(m))) for s,p in perm(n))

def smith(X, j, t):
    
    j0 = j[t-1]+1 if t > 0 else 0

    for j in range(j0, n):
        if numpy.any(X[:,j]):
            j[t] = j
            break

def submatricies(X, i):
    
    m,n = numpy.shape(X)
    
    for cr in itertools.combinations(range(m),i):
        for cc in itertools.combinations(range(n),i):
            yield X[numpy.ix_(cr,cc)]

def minors(X, i):
    for sm in submatricies(X, i):
        #yield int(numpy.linalg.det(sm))
        yield determinant(sm)

def determinant_divisor(X, i):
    
    if i == 0: return 1

    d = None

    for m in minors(X, i):
        #print('minor',m)
        if d is None:
            d = m
        else:
            d = math.gcd(m, d)
        #print('d',d)

    return d

def smith(X):
    print('determinant divisors')

    d = list(determinant_divisor(X, i) for i in range(min(numpy.shape(X))))

    print(d)

X=numpy.arange(12, dtype=numpy.int64).reshape((4,3))

X = numpy.empty(shape=(4,4), dtype=numpy.int64)

s = sympy.symbols('a b')

print(s)

X[0,0] = 1
X[0,1] = 2
X[0,2] = 3
X[0,3] = 4
X[1,0] = 3
X[1,1] = 4
X[1,2] = 1
X[1,3] = 2
X[2,0] = 4
X[2,1] = 3
X[2,2] = 2
X[2,3] = 1
X[3,0] = 2
X[3,1] = 1
X[3,2] = 4
X[3,3] = 3

print(X)

smith(X)

print(list(itertools.permutations(range(3))))
print(list(perm(3)))




