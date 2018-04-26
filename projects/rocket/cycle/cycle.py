import itertools
import sys
import io
import contextlib

import scipy.optimize
from CoolProp.CoolProp import PropsSI
import numpy as np
import matplotlib.pyplot as plt

from .propellants import *
from .point import *
from .components import *

def breakpoint(): import pdb; pdb.set_trace();

def point_tank(f):
    p = Point(0, f)
    p.T = 293
    p.p = 10e5
    p.m = 2 # kg / s
    return p

class Cycle:
    def __init__(self, n, energy_comb_frac=0.005):
        self.prop = PropEthanolLOX()
        self.p = [Point(i, self.prop.f.s) for i in range(n)]

        self.p[0] = point_tank(self.prop.f.s)

        assert self.p[0] != self.p[1]
        assert self.p[0]._functions_p is not self.p[1]._functions_p

        self.energy_comb = self.prop.h * (self.p[0].m + self.p[0].m / self.prop.mass_ratio)
    
        self.q_chamber = self.energy_comb * energy_comb_frac

        self.p_chamber = 6.89e6

    def clear(self):
        for p in self.p[1:]:
            for s in ['T', 'p', 'm', 's', 'h']:
                p.clear(s)

    def power_frac(self):
        return self.turb.power() / self.pump.power()

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

    def solve(self):

        y = self.do(self.x_0)

        assert y != [0]

        #o = io.StringIO()
        #with contextlib.redirect_stdout(o):
        res = scipy.optimize.fsolve(self.do, self.x_0)

        #s = o.getvalue()

        self.do(res)

class OpenDecoupled(Cycle):
    def __init__(self, pr=None, **kwargs):
        super(OpenDecoupled, self).__init__(4, **kwargs)

        self.pr = pr

        self.pump = Pump(self.p[0], self.p[1], 0.8)
    
        Heat(self.p[1], self.p[2], self.q_chamber)
    
        self.turb = Turbine(self.p[2], self.p[3], 0.9)

    def do(self):
        self.clear()

        self.p[3].p = self.p_chamber

        self.p[1].p = self.p[2].p = self.p[3].p * self.pr

class ClosedDecoupledPreheat(Cycle):
    def __init__(self, bypass=None, **kwargs):
        super(ClosedDecoupledPreheat, self).__init__(9, **kwargs)
        
        self._bypass = bypass

        Mix(self.p[0], self.p[8], self.p[1])
    
        self.pump = Pump(self.p[1], self.p[2], 0.8)
    
        equal([self.p[2], self.p[3]], 'p')
        equal([self.p[2], self.p[3]], 'h')

        Heat(self.p[3], self.p[4], self.q_chamber)

        Split(self.p[4], self.p[5], self.p[6], lambda: 1 - self.bypass())

        #p[5].h = p[6].h = p[4].h
    
        self.turb = Turbine(self.p[6], self.p[7], 0.9)

        equal([self.p[7], self.p[8]], 'p')

        equal([self.p[0], self.p[5]], 'm')
        equal([self.p[1], self.p[4]], 'm')

        self.x_0 = [5000]

    def bypass(self):
        return self._bypass

    def do(self, x):

        self.clear()

        self.p[7]._guess['h'] = x[0]

        self.p[5].p = self.p_chamber

        self.p[8].T = self.p[0].T + 5
               
        self.p[4].m
        self.p[6].m

        self.p[7].p

        self.p[7].p

        self.p[1].m
        self.p[2].h
        self.p[3].h
        self.p[4].h
        self.p[6].h
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



