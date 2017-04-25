#!/usr/bin/env python3
import math
import numpy
import matplotlib.pyplot as plt

def func(r_e, r, d):
    f = 0.5 * (1.0 + d)
    return r_e*(r_e-r)/(r_e-f*r)

def func_r_ex(r_1, r_2, d):
    f = 0.5 * (1.0 + d)
    D = (r_1 + r_2) / 2.0
    E = numpy.sqrt(numpy.power(r_1 + r_2,2.0) - 4.0 * f * r_1 * r_2) / 2.0
    return D,E

def func_r_ex_1(r_1, r_2, d):
    D, E = func_r_ex(r_1, r_2, d)
    return D + E

def func_r_ex_2(r_1, r_2, d):
    D, E = func_r_ex(r_1, r_2, d)
    return D - E


r_1 = 1.0
d = 0.7
f = 0.5 * (1.0 + d)

r_2 = numpy.logspace(-5.0,5.0,100)

r_a = func_r_ex_1(r_1, r_2, d)
r_p = func_r_ex_2(r_1, r_2, d)

print('r_p limit ',r_p[-1])
print('r_1 f     ',r_1 * f)

if 0:
    
    #plt.plot(r_2, r_p)
    #plt.plot(r_2, r_a)
    plt.loglog(r_2, r_p)
    plt.loglog(r_2, r_a)
    
    plt.figure()
    
    plt.loglog(r_2, func(r_p, r_2, d))
    plt.loglog(r_2, func(r_a, r_2, d))
    plt.loglog(r_2, func(r_p, r_1, d))
    plt.loglog(r_2, func(r_a, r_1, d))
    
    plt.figure()
    
    plt.loglog(r_p, func(r_p, r_1, d))
    
    plt.figure()
    
    plt.loglog(r_a, func(r_a, r_1, d))
    

plt.figure()

r_e = numpy.logspace(-1.0,1.0,1000)
r_2 = func(r_e, r_1, d)
plt.loglog(r_e, r_2)
plt.loglog(r_1*f*numpy.ones(numpy.shape(r_e)),r_2)
plt.loglog(r_1*numpy.ones(numpy.shape(r_e)),r_2)
plt.xlabel('r_p left of the gap, r_a right of the gap. gap extends from r_1*f to r_1')
plt.ylabel('r_2')

plt.show()

