# -*- coding: utf-8 -*-
"""
Created on Thu Mar 09 13:37:34 2017

@author: msimones
"""
from __future__ import division
from scipy import optimize
import numpy as np
import matplotlib.pyplot as plt

#Example from "Refrigeration and Air Conditioning", Stoecker

def qe_comp(te, tc): #compressor capacity rating function
    c1 = 137.402;
    c2 = 4.60437;
    c3 = 0.061652;
    c4 = -1.118157;
    c5 = -0.001525;
    c6 = -0.0109119;
    c7 = -0.00040148;
    c8 = -0.00026682;
    c9 = 0.000003873;
    return c1+c2*te+c3*te**2+c4*tc+c5*tc**2+c6*te*tc+c7*te**2*tc+c8*te*tc**2+c9*te**2*tc**2
    
def p(te,tc): #compressor power rating function
    d1 = 1.00618;
    d2 = -0.893222;
    d3 = -0.01426;
    d4 = 0.870024;
    d5 = -0.0063397;
    d6 = 0.033889;
    d7 = -0.00023875;
    d8 = -0.00014746;
    d9 = 0.0000067962;
    return d1+d2*te+d3*te**2+d4*tc+d5*tc**2+d6*te*tc+d7*te**2*tc+d8*te*tc**2+d9*te**2*tc**2

def qc(tc, tamb): #condenser rating function
    F = 9.39;
    return F*(tc-tamb)
    
def qe(te, twin): #evaporator rating function
    return 6.0*(1+0.046*(twin-te))*(twin-te)
    
def fun(x): #refr. system balance
    tamb = 35;
    twin = 20;
    tloss = 2;
    return [qe_comp(x[4]+tloss,x[3])-x[0],
            p(x[4]+tloss,x[3])-x[1],
            x[2]-x[0]-x[1],#conservation of energy
            qc(x[3],tamb)-x[2],
            qe(x[4],twin)-x[0]]
x_guess = [100,20,200,40,15]
sol = optimize.root(fun,x_guess)
print sol.x

