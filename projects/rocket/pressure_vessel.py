import numpy
import math
import scipy.optimize

def length(X, V, r):
    L = X[0]
    
    V2 = 4.0/3.0 * math.pi * r**3.0 + math.pi * r**2.0 * L

    return V - V2

############################

P = 8e6
r = 0.15
V = 0.1

s_Y = 276e6

sf = 4.0

s = s_Y / sf

t = P * r / s

L = scipy.optimize.fsolve(length, [.1], (V, r))[0]

print "t",t
print "L",L



