__version__ = '0.1a0'
import argparse
import numpy as np
import os
import math
import scipy.stats
import matplotlib.pyplot as plt
import sys

class LinearRegression:
    """
    x must be column vectors
    """
    def calc(self):
        X0 = self.x
        Y = self.y
        
        print('x shape',np.shape(X0))

        self.n = np.shape(Y)[0]
    
        Y = np.reshape(Y, (self.n, 1))

        try:
            X = self.X
            self.k = np.shape(X)[1]
        except:
            if(len(np.shape(X0)) == 1):
                self.k = 2
            else:
                if np.shape(X0)[0] == 1:
                    self.k = np.shape(X0)[0] + 1
                else:
                    self.k = np.shape(X0)[1] + 1

            X0 = np.reshape(X0, (self.n, self.k - 1))
            X = np.append(np.ones((self.n,1)), X0, 1)

        try:
            A = self.A
        except:
            try:
                W = self.W
            except:
                A = np.identity(self.n)
            else:
                A = np.dot(W,W)


        Xt = np.transpose(X)

        Ci = np.dot(np.dot(Xt, A), X)
        
        C = np.linalg.inv(Ci)

        if 0:       
            if A[0,0] != 0:

                UU1 = np.dot(Xt, X)
                UU2 = np.dot(X, Xt)

                print("UU1")
                print(UU1)
                print("UU2")
                print(UU2)

                A2 = np.diag(np.power(np.diag(A), -1.0))
            
                C2 = np.dot(np.dot(Xt, A2), X)
                
                print("A")
                print(A)
                print("A2")
                print(A2)
                print("C")
                print(C)
                print("C2")
                print(C2)
    
                sys.exit(0)

        self.D = np.dot(np.dot(C, Xt), A)
        
        # coefficients of the curve fit line
        self.B = np.dot(self.D,Y)
        
        # distance from y data to curve-fit line
        e = Y - np.dot(X,self.B)
    
        # sigma^2
        self.v = np.dot(np.transpose(e), e)[0,0] / float(self.n-self.k)
        
        self.t = scipy.stats.t.ppf(1-0.025, self.n-self.k)
        
        if 0:
            print("shape(X)", np.shape(X))
            print("shape(Y)", np.shape(Y))
            print("shape(B)", np.shape(self.B))
            print("shape(e)", np.shape(e))
            print("v       ", self.v)
            print("t       ", self.t)
        
        # cov = sigma^2 D D'
        self.cov = self.v * np.dot(self.D, np.transpose(self.D))
    
    def calc2(self, *args):

        n = len(args[0])

        X = np.ones((n,1))
        for x in args: 
            X = np.append(X, np.reshape(x, (n,1)), 1)

        return self.response3(X)

    def response(self, x0, B=None):
        print('response x0 shape', np.shape(x0))
        s = np.shape(x0)
        n0 = s[0]
        x0 = np.reshape(x0, (n0, self.k-1))
        x0 = np.append(np.ones((n0,1)), x0, 1)
        
        return self.response2(x0, B)
    
    def response2(self, x0, B=None):
        if B is None: B = self.B

        n0 = np.shape(x0)[0]

        x0t = np.transpose(x0)

        y = np.dot(x0, B)
        
        v0 = np.reshape(np.diagonal(np.dot(np.dot(x0, self.cov), x0t)), (n0,1))

        s0 = np.sqrt(v0)

        return y, self.t * s0

    def response3(self, x0):

        n0 = np.shape(x0)[0]

        x0t = np.transpose(x0)

        y = np.dot(x0,self.B)
        
        return y

def linreg(*args):

    y = args[0]

    n = len(y)

    args = args[1:]

    Y = np.reshape(y, (n,1))

    X = np.ones((n,1))
    for x in args: 
        X = np.append(X, np.reshape(x, (n,1)), 1)

    l = LinearRegression()

    l.X = X
    l.Y = Y

    l.calc()

    return l


