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

def point_tank_f(f):
    p = Point(0, f)
    p.T = 293
    p.p = 10e5
    p.m = 2 # kg / s
    return p

def point_tank_o(i, f):
    p = Point(i, f)
    p.Q = 0
    p.p = 10e5
    p.m = 2 # kg / s
    return p

class Cycle:
    def __init__(self, n_f, n_o, energy_comb_frac=0.005):
        self.prop = PropEthanolLOX()
        
        self.n_f = n_f

        self.p_f = [Point(i, self.prop.f.s) for i in range(n_f)] 
        self.p_o = [Point(i + n_f, self.prop.o.s) for i in range(n_o)]
 
        self.p_f[0] = point_tank_f(self.prop.f.s)
        self.p_o[0] = point_tank_o(4, self.prop.o.s)

        self.p = self.p_f + self.p_o

        assert self.p[0] != self.p[1]
        assert self.p[0]._functions['p'] is not self.p[1]._functions['p']

        self.energy_comb = self.prop.h * (self.p[0].m + self.p[0].m / self.prop.mass_ratio)
    
        self.q_chamber = self.energy_comb * energy_comb_frac

        self.p_chamber = 6.89e6

    def clear(self):
        for i in range(len(self.p)):
            if i == 0: continue
            if i == self.n_f: continue
            p = self.p[i]
            for s in ['T', 'p', 'm', 's', 'h']:
                p.clear(s)

        for c in self.components:
            c.clear()

    def power_frac(self):
        p_o = self.pump_o.power()
        return self.turb.power() / (self.pump.power() + p_o)

    def print_(self):
        #print(f'enery comb    {energy_comb:10.0f}')
        #print(f'q_chamber     {q_chamber:10.0f}')
        print(f'pump power    {self.pump.power():10.0f}')
        print(f'pump o power  {self.pump_o.power():10.0f}')
        print(f'turbine power {self.turb.power():10.0f}')
        print(f'power frac    {self.power_frac():10.3f}')

        print(f'{"points":10} {"p":>10} {"T":>10} {"m":>12} {"h":>10} {"s":>10}')
        for i in range(len(self.p_f)):
            p_ = self.p_f[i]
            p_.p
            p_.T
            p_.m
            p_.h
            p_.s
            print(f'{i!s:10} {p_.p:10.0f} {p_.T:10.0f} {p_.m:12.3f} {p_.h:10.0f} {p_.s:10.0f}')

        print(f'{"points":10} {"p":>10} {"T":>10} {"m":>12} {"h":>10} {"s":>10}')
        for i in range(len(self.p_o)):
            p_ = self.p_o[i]
            p_.p
            p_.T
            p_.m
            p_.h
            p_.s
            print(f'{i!s:10} {p_.p:10.0f} {p_.T:10.0f} {p_.m:12.3f} {p_.h:10.0f} {p_.s:10.0f}')

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

        assert not np.all(y == 0)

        #o = io.StringIO()
        #with contextlib.redirect_stdout(o):
        res = scipy.optimize.fsolve(self.do, self.x_0)

        #s = o.getvalue()

        self.do(res)

class OpenDecoupled(Cycle):
    def __init__(self, pr=None, power_frac=None, **kwargs):
        super(OpenDecoupled, self).__init__(4, 2, **kwargs)

        self._pr = pr
        self._power_frac = power_frac

        self.pump = Pump(self.p[0], self.p[1])
    
        self.heat_chamber = Heat(self.p[1], self.p[2])

        self.turb = Turbine(self.p[2], self.p[3], 0.9)

        self.pump_o = Pump(self.p_o[0], self.p_o[1])

        self.components = [self.heat_chamber]

    def print_(self):
        print(f'pr            {self.pr():13.2f}')
        print(f'heat chamber  {self.heat_chamber.q:13.2f}')
        super(OpenDecoupled, self).print_()
 
    def pr(self):
        return self._pr or self.x[0]

    @property
    def x_0(self):
        return [1.2]

    def do(self, x):
        self.x = x

        self.clear()

        self.heat_chamber.q = self.q_chamber

        self.p[3].p = self.p_chamber

        self.p_o[1].p = self.p_chamber

        self.p[1].p = self.p[2].p = self.p[3].p * self.pr()

        y = np.array([
            (self._power_frac or self.power_frac()) - self.power_frac(),
            ])

        return y

class ClosedDecoupledPreheat(Cycle):
    def __init__(self, bypass=None, power_frac=None, **kwargs):
        super(ClosedDecoupledPreheat, self).__init__(9, 3, **kwargs)
        
        self._bypass = bypass
        self._power_frac = power_frac

        Mix(self.p[0], self.p[8], self.p[1])
    
        self.pump = Pump(self.p[1], self.p[2], 0.8)
    
        equal([self.p[2], self.p[3]], 'p')
        equal([self.p[2], self.p[3]], 'h')

        self.heat_chamber = Heat(self.p[3], self.p[4])

        Split(self.p[4], self.p[5], self.p[6], lambda: 1 - self.bypass())

        self.turb = Turbine(self.p[6], self.p[7], 0.9)

        self.heat_condenser = Heat(self.p[7], self.p[8])

        equal([self.p[0], self.p[5]], 'm')
        equal([self.p[1], self.p[4]], 'm')

        # oxidizer loop
        
        self.pump_o = Pump(self.p_o[0], self.p_o[1])

        self.heat_condenser_o = Heat(self.p_o[1], self.p_o[2])

        # couple the condenser sides
        self.heat_condenser._functions['q'].append(lambda c: -self.heat_condenser_o.q)
        self.heat_condenser_o._functions['q'].append(lambda c: -self.heat_condenser.q)

        self.components = [self.heat_chamber]

    @property
    def x_0(self):
        if self._bypass is not None:
            return [5000]
        else:
            return [5000, 0.05]

    def print_(self):
        print(f'bypass        {self.bypass():15.4f}')
        print(f'q condenser   {self.heat_condenser.q:15.4f}')
        print(f'heat chamber  {self.heat_chamber.q:13.2f}')
        print(f'              {flow_power(self.p_f[0], self.p_f[5]):13.2f}')
        super(ClosedDecoupledPreheat, self).print_()
 
    def bypass(self):
        return self._bypass or self.x[1]

    def do(self, x):
        self.x = x
        self.clear()

        self.heat_chamber.q = self.q_chamber

        self.p[7]._guess['h'] = x[0]

        self.p[5].p = self.p_chamber

        self.p_o[2].p = self.p_chamber

        self.p[8].T = self.p[0].T + 0
               
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
        
        if self._bypass is not None:
            y = np.array([
                self.p[7].h - x[0],
                ])
        else:
            y = np.array([
                self.p[7].h - x[0],
                self.power_frac() - self._power_frac,
                ])
        
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

        return y



