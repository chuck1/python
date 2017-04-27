#!/usr/bin/env python3

import math
import numpy
import matplotlib.pyplot as plt

import ksp

def func(y, v, theta, mu, a):
    
    dt = 0.05

    x = 0

    v_x = v * math.cos(theta)
    v_y = v * math.sin(theta)
    
    r = math.sqrt(x**2+y**2)

    t = 0

    while v_y < -1:
        
        a_x = -a * math.cos(theta)
        a_y = -a * math.sin(theta) - mu/r/r
        
        x += v_x * dt
        y += v_y * dt
    
        v_x += a_x * dt
        v_y += a_y * dt

        r = math.sqrt(x**2+y**2)
        
        t += dt

    return r,t

def study_theta(ax_r, ax_t, v):
    y = 100000
    theta = -math.pi/4
    mu = 1E10
    a = 10
    
    v_func = numpy.vectorize(func)
    
    #theta = -math.pi/2*numpy.logspace(-2,0)
    theta = numpy.linspace(-0.3,-math.pi/2)
    
    r,t = v_func(y, v, theta, mu, a)
    
    X = -numpy.sin(theta)
    X_str = '-sin(theta)'
    
    c = numpy.polyfit(X,r,1)
    
    print(c)
    print(c[0]/v)
    
    p = numpy.poly1d(c)

    ax_r.plot(X,r,'-o',label="v={}".format(v))
    ax_r.plot(X,p(X),'-',label="v={}".format(v))
    ax_r.set_xlabel(X_str)
    ax_r.set_ylabel('r')

    if ax_t:
        ax_t.loglog(X,t,'-o',label="v={}".format(v))
        ax_t.set_xlabel(X_str)
        ax_t.set_ylabel('t')

    return c

fig = plt.figure()

ax_r = fig.add_subplot(1,1,1)

#fig = plt.figure()

#ax_t = fig.add_subplot(1,1,1)
ax_t = None

V = numpy.linspace(100,300,10)

c = numpy.array([study_theta(ax_r, ax_t, v) for v in V])

print(c)

ax_r.legend()

plt.figure()
plt.loglog(V,-c[:,0],'o')

plt.show()





