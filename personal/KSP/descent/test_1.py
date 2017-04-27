#!/usr/bin/env python3

import matplotlib.pyplot as plt

import math
import numpy

import ksp

def descent(y, v_x, v_y, ship_a, mu):
    
    vec_r = numpy.array([0.,y])
    vec_v = numpy.array([v_x,v_y])

    dt = 0.1
    t = 0
    
    d = numpy.dot(vec_r, vec_v)
    r = numpy.linalg.norm(vec_r)
    v = numpy.linalg.norm(vec_v)
    
    r0 = r

    while (d < 0) and (v > 1):
        
        vec_a = -vec_v / v * ship_a - mu / numpy.power(r,3) * vec_r
        
        vec_r += vec_v * dt
        vec_v += vec_a * dt
        
        d = numpy.dot(vec_r, vec_v)
        r = numpy.linalg.norm(vec_r)
        v = numpy.linalg.norm(vec_v)

        t += dt

    if 0:
        print('t    ',t)
        print('vec_r',vec_r)
        print('vec_v',vec_v)
        print('r0   ',r0)
        print('r    ',r)

    return r,t

body = ksp.mun

#y = numpy.linspace(200000,210000,100)
y = 210000

a = numpy.linspace(3,10,10)

vec_descent = numpy.vectorize(descent)

r,t = vec_descent(y,200.,-1.,a,body.mu)

plt.plot(a,r)
plt.figure()
plt.plot(a,t)

plt.show()




