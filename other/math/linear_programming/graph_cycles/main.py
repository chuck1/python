import numpy
import scipy.optimize

c = -1*numpy.ones((5,))

print(c)

M = numpy.array([
    [1, 0, 0, 1, 1],
    [1, 1, 0, 0, 0],
    [0, 1, 1, 0, 1],
    [0, 0, 1, 1, 0]
    ])

m = numpy.ones((4, 1)) * 2

N = numpy.identity(5)

n = numpy.ones((5, 1))

A = numpy.concatenate((M, N), axis=0)
b = numpy.concatenate((m, n), axis=0)

print(A)
print(b)
print(c)

x = scipy.optimize.linprog(c, A, b)

print(x)

