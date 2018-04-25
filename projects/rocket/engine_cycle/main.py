import itertools
import sys
import io
import contextlib

import scipy.optimize
from CoolProp.CoolProp import PropsSI
import numpy as np
import matplotlib.pyplot as plt

from propellants import *
from point import *
from components import *

def breakpoint(): import pdb; pdb.set_trace();

def point_tank(f):
    p = Point(0, f)
    p.T = 293
    p.p = 10e5
    p.m = 2 # kg / s
    return p


class Cycle:
    def __init__(self, n):
        self.prop = PropEthanolLOX()
        self.p = [Point(i, self.prop.f.s) for i in range(n)]
        self.p[0] = point_tank(self.prop.f.s)

        assert self.p[0] != self.p[1]
        assert self.p[0]._functions_p is not self.p[1]._functions_p

        self.energy_comb = self.prop.h * (self.p[0].m + self.p[0].m / self.prop.mass_ratio)
    
        self.q_chamber = self.energy_comb * 0.0015

    def clear(self):
        for p in self.p[1:]:
            for s in ['T', 'p', 'm', 's', 'h']:
                p.clear(s)

    def setup_0(self):

        p_chamber = 6.89e6
    
        return self.prop, self.q_chamber, p_chamber, self.energy_comb

    def print_(self):
        #print(f'enery comb    {energy_comb:10.0f}')
        #print(f'q_chamber     {q_chamber:10.0f}')
        print(f'pump power    {self.pump.power():10.0f}')
        print(f'turbine power {self.turb.power():10.0f}')
        print(f'power frac    {self.turb.power() / self.pump.power():10.3f}')

        print(f'{"points":10} {"p":>10} {"T":>10} {"m":>12} {"h":>10} {"s":>10}')
        for i in range(len(self.p)):
            p_ = self.p[i]
            p_.p
            p_.T
            p_.m
            p_.h
            p_.s
            print(f'{i!s:10} {p_.p:10.0f} {p_.T:10.0f} {p_.m:12.1f} {p_.h:10.0f} {p_.s:10.0f}')

        print()

    def plot(self):
        fig, axs = plt.subplots(1, 1)
        
        ax = axs

        for i in range(len(p)):
            ax.plot(p[i].s, p[i].T, 'o')
            ax.annotate(str(i), (p[i].s, p[i].T))

        plt.show()

class OpenDecoupled(Cycle):

    def do(self, pr_turb):
    
        prop, q_chamber, p_chamber, energy_comb = self.setup_0()
    
        self.p[3].p = p_chamber
        self.p[1].p = self.p[2].p = self.p[3].p * pr_turb
    
        self.pump = Pump(self.p[0], self.p[1], 0.8)
    
        Heat(self.p[1], self.p[2], q_chamber)
    
        self.turb = Turbine(self.p[2], self.p[3], 0.9)

class ClosedDecoupledPreheat(Cycle):
    def __init__(self):
        super(ClosedDecoupledPreheat, self).__init__(9)


        Mix(self.p[0], self.p[8], self.p[1])
    
        self.pump = Pump(self.p[1], self.p[2], 0.8)
    
        equal([self.p[2], self.p[3]], 'p')
        equal([self.p[2], self.p[3]], 'h')

        Heat(self.p[3], self.p[4], self.q_chamber)

        Split(self.p[4], self.p[5], self.p[6], 2, 1)

        #p[5].h = p[6].h = p[4].h
    
        self.turb = Turbine(self.p[6], self.p[7], 0.9)

        equal([self.p[7], self.p[8]], 'p')

    def do(self, x, bypass_fraction):

        prop, q_chamber, p_chamber, energy_comb = self.setup_0()
        
        self.clear()

        self.p[7]._guess['h'] = x[0]
        #p[7]._volatile_h = True
        
        #print()
        #print(self.p[7].h)


        self.p[5].p = p_chamber

        self.p[5].m = self.p[0].m
        self.p[6].m = self.p[5].m * 0.5
        self.p[4].m = self.p[5].m + self.p[6].m
        self.p[1].m = self.p[4].m

        self.p[8].T = self.p[0].T + 5
    
        #p[6].m = p[8].m = p[0].m * bypass_fraction
    
        #p[1].p = p[7].p = p[8].p = p[0].p
        #p[2].p = p[3].p = p[4].p = p[5].p = p[6].p = p_chamber
        


        #self.p[3] = self.p[2]
    

        self.p[7].p

        self.p[7].p
        self.p[6].s
        
        y = np.array([self.p[7].h])
        
        self.p[0].h
        self.p[7].h
        self.p[7].s
        self.p[8].T
        self.p[8].p
        self.p[8].h
        self.p[1].h


        self.p[4].p
        self.p[3].p
        self.p[2].p
        self.p[2].h

        self.pump.power()

        return y - x

def solve(c, x_0, args, plot=False):

    y = c.do(x_0, *args)

    assert y != [0]

    #o = io.StringIO()
    #with contextlib.redirect_stdout(o):
    res = scipy.optimize.fsolve(c.do, x_0, args)

    #s = o.getvalue()

    print(res)
    
    print(c.do(res, *args))

    if plot:
        c.plot()

c0 = OpenDecoupled(4)
c0.do(2.0)

c0.print_()

#partial_closed_decoupled(0)

#solve(partial_closed_decoupled, [70000], (1.0,))

#partial_closed_decoupled_preheat([50000, 40000], 0.5)

c1 = ClosedDecoupledPreheat()

solve(c1, [50000], (0.5,))

c1.print_()

