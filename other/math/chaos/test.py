#!/usr/bin/env python3
import math
import numpy
import matplotlib.pyplot as plt
import random
import argparse

random.seed()

class Draw(object):
    def __init__(self, P, X, f):
        self.P=P
        self.X=X
        self.f=f

    def step(self, m):
        n = numpy.shape(self.P)[0]

        for i in range(m):
            j = random.randint(0,n-1)
        
            x = self.X[-1,:]
        
            p = self.P[j,:]
        
            v = p - x
            
            x = x + self.f * v
            
            self.X = numpy.append(self.X,numpy.reshape(x,(1,2)),axis=0)

    def plot(self):
        plt.plot(self.P[:,0],self.P[:,1],'o')
        plt.plot(self.X[:,0],self.X[:,1],'o',markersize=5)
        plt.show()

if __name__=='__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('n',type=int)
    parser.add_argument('f',type=float)
    args = parser.parse_args()
    
    x = numpy.cos(numpy.linspace(0,math.pi*(2-2/args.n),args.n))
    y = numpy.sin(numpy.linspace(0,math.pi*(2-2/args.n),args.n))
    X = numpy.append(numpy.reshape(x,(args.n,1)),numpy.reshape(y,(args.n,1)),axis=1)
    
    x = 2*numpy.cos(numpy.linspace(0,math.pi*(2-2/(args.n+1)),args.n+1))
    y = 2*numpy.sin(numpy.linspace(0,math.pi*(2-2/(args.n+1)),args.n+1))
    X = numpy.append(X,numpy.append(numpy.reshape(x,(args.n+1,1)),numpy.reshape(y,(args.n+1,1)),axis=1),axis=0)
    
    draw = Draw(
            X,
            numpy.array([[0,0]]),
            args.f)

    draw.step(10000)

    draw.plot()



