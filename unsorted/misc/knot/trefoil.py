import math
import pylab as pl
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def polar(t):
    #return 1
    a = 0.8 + 0.2 * math.sin(1.5 * t)
    b = 5.0
    f = 1.5
    b = 1.0 + 0.2 * math.sqrt((1.0+b**2)/(1.0+b**2*math.sin(f * t)**2)) * math.sin(f * t)
    return a
    
    
    
def func_z(t):
    return 0.2 * math.cos(3./2.*t)

def polar_to_cart_x(t,r):
    return r*math.cos(t)

def polar_to_cart_y(t,r):
    return r*math.sin(t)

f = np.vectorize(polar)
fx = np.vectorize(polar_to_cart_x)
fy = np.vectorize(polar_to_cart_y)
fz = np.vectorize(func_z)

t = np.linspace(0,4.0*math.pi,400)

r = f(t)

x = fx(t,r)
y = fy(t,r)
z = fz(t)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt.plot(x,y,z)
b=[-1.5,1.5]
plt.plot(b,b,b)

pl.figure()
pl.plot(t,r)

pl.show()



