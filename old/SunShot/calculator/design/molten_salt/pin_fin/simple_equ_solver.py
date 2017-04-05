#!/usr/bin/env python
import Sci.Fluids as fl
import math
import numpy as np
import Sci.Solve.shooting as sh

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-p',action='store_true')
args = parser.parse_args()

if args.p:
    import pylab as pl

p = np.load('p.npy')

print "p =",p

k = 1.5008651836e-08
a = 3.33789953302
b = -2.27768731053


# knowns
PT = 1.5
L = 1e-2
qpp = 4e6
dp_target = 0.5 * 100000
T1 = 573.15
T2 = 873.15
flu = fl.Fluid("ms1")

# find D


# dp as function of D and constants
# log(dp) = f(log(D))
def func_dp(D):
    
    rho = flu.get('density', T1)

    ST = D * PT
    PL = math.sqrt(3.0) / 2.0 * PT
    SL = PL * D

    A_heated = L * ST / 2.0

    dh = flu.enthalpy_change(T1,T2)
    
    md = qpp * A_heated / dh

    GAP = ST - D
    
    A_min_flow = 3.1415 * GAP**2 / 4.0

    v = md / A_min_flow / rho

    KE = rho * v**2 / 2.0
    
    f = k * PT**a * D**b
    
    #print "f =",f
    
    NL = L / SL

    dp = KE * f * NL
   
    return dp


def func_dp_linearized(obj,logD):
    
    D = math.exp(logD)
    
    dp = func_dp(D)

    return math.log(dp_target) - math.log(dp)
    

# initial guess


logD = sh.shooting(0, np.log([3.0e-4, 1.0e-3]), func_dp_linearized)
D = math.exp(logD)

dp = func_dp(D)

print "D  = {0: e}".format(D)
print "PT = {0: e}".format(PT)
print "L  = {0: e}".format(L)
print "dp = {0: e}".format(dp)




