#!/usr/bin/env python3
import math
import numpy
import matplotlib.pyplot as plt

class Ellipse(object):
    def __init__(self, r_a, r_1, d):
        self.r_a = r_a
        self.r_1 = r_1
        self.d = d

    def calc(self):
        f = self.r_a / self.r_1

        self.r_2 = self.r_a * (f-1) / (f - 0.5*(1 + self.d))
        
        print('r_1',self.r_1)
        print('r_2',self.r_2)

        self.a = 0.5*(self.r_1 + self.r_2)

        self.c = self.r_a - self.a
        
        self.b = math.sqrt(self.a**2 - self.c**2)
        
        print('a',self.a)
        print('b',self.b)
        print('c',self.c)

    def plot(self):
        t = numpy.linspace(0,2.0*math.pi,100)
        plt.plot(self.a * numpy.cos(t), self.b * numpy.sin(t))


r_a = 1.

#a = 2.
a = numpy.linspace(2., 0.2, 100)

#d = numpy.linspace(0,1,100)
d = 0.1

#r_2 = func(r_a, r_a/a, d)

#plt.plot(a, r_2)
#plt.show()


plt.plot(0,0,'o')

for r_a in [1.5, 1.4]:
    e = Ellipse(r_a, 1.0, 0.5)
    e.calc()
    e.plot()




plt.show()


