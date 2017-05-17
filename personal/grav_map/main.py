import math
import matplotlib
import numpy as np

import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

G = 6.78e-11

class Sat(object):
    def __init__(self, x, y, m):
        self.x = x
        self.y = y
        self.m = m
    
    def e(self, x, y):
        dx = self.x-x
        dy = self.y-y
        r = math.sqrt(dx**2 + dy**2)
        if r == 0:
            return 0
        return math.log(G * self.m / r)

earth = Sat(0,0,6e24)
moon = Sat(0,3.8e8,7.3e22)

def func(x,y):
    return earth.e(x,y) + moon.e(x,y)


d = 1e10

x = np.linspace(-d, d, 1000)
y = np.linspace(-d, d, 1000)

X,Y = np.meshgrid(x,y)

#print x,y
#print X,Y

vfunc = np.vectorize(func)

Z = vfunc(X,Y)

plt.figure()
CS = plt.contourf(X,Y,Z,40)
plt.show()



