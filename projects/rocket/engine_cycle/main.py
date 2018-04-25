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

def breakpoint(): import pdb; pdb.set_trace();

class Pump:
    def __init__(self, p0, p1, e):
        self.p0 = p0
        self.p1 = p1

        equal([p0, p1], 'm')
         
        def _h(p1):
            p1.h_s = PropsSI("H", "P", p1.p, "S", p0.s, p1.f)
            return (p1.h_s - p0.h + p0.h * e) / e

        p1._functions_h.append(_h)

    def power(self):
        return flow_power(self.p0, self.p1)

def _turbine_h(p, p0, p1, e):
    assert p is p1
    assert p is not p0
    try:
        h_1s = PropsSI("H", "P", p1.p, "S", p0.s, p1.f)
        h_1 = p0.h - e * p0.h + e * h_1s
        print('turbine enthalpy equation', h_1)
        return h_1
    except Exception as ex:
        print(ex)
        raise

class Turbine:
    def __init__(self, p0, p1, e):
        self.p0 = p0
        self.p1 = p1

        equal([p0, p1], 'm')

        p1._functions_h.append(lambda p: _turbine_h(p, p0, p1, e))

    def power(self):
        return -flow_power(self.p0, self.p1)

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

def point_tank(f):
    p = Point(0, f)
    p.T = 293
    p.p = 10e5
    p.m = 2 # kg / s
    return p

class Heat:
    def __init__(self, p0, p1, q):
        equal([p0, p1], 'm')
        equal([p0, p1], 'p')
        p1._functions_h.append(lambda p: p0.h + q * p0.m)

def flow_power(p0, p1):
    p0.m
    p0.h
    p1.h
    return p0.m * (p1.h - p0.h)

class Mix:
    def __init__(self, p0, p1, p2):
        equal([p0, p1, p2], 'p')

        p2._functions_m.append(lambda p: p0.m + p1.m)
        p0._functions_m.append(lambda p: p2.m - p1.m)
        p1._functions_m.append(lambda p: p2.m - p0.m)

        p2._functions_h.append(lambda p: (p0.h * p0.m + p1.h * p1.m) / p2.m)

def _f(p, p0, p1, s):
    #print(f'{p}.{s} = {p1}.{s}')
    assert p is p0
    assert p is not p1
    return getattr(p1, s)

def equal1(p0, p1, s):
        assert p0 is not p1
        
        l0 = getattr(p0, '_functions_' + s)
        l1 = getattr(p1, '_functions_' + s)

        assert l0 is not l1

        getattr(p0, '_functions_' + s).append(lambda p: _f(p, p0, p1, s))

def equal(pts, s):
    for i, j in itertools.permutations(range(len(pts)), 2):
        p0 = pts[i]
        p1 = pts[j]
        
        equal1(p0, p1, s)

class Split:
    def __init__(self, p0, p1, p2, f1, f2):
        
        p0._functions_m.append(lambda p: p1.m / f1 * (f1 + f2))
        p0._functions_m.append(lambda p: p2.m / f2 * (f1 + f2))

        p1._functions_m.append(lambda p: p0.m * f1 / (f1 + f2))
        p2._functions_m.append(lambda p: p0.m * f2 / (f1 + f2))
        
        equal([p0, p1, p2], 'p')
        equal([p0, p1, p2], 'T')
        equal([p0, p1, p2], 'h')
        equal([p0, p1, p2], 's')

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


        #print(self.p[0].h)
        #print(self.p[8].h)
        #print(self.p[1].h)
        #print(self.p[2].h)
        #print(self.p[3].h)
        #print(self.p[4].h)
        
        #print(self.p[6].h)

        self.p[7].p
        self.p[6].s
        
        #print(self.p[7].h)
        
        #breakpoint()

        y = np.array([self.p[7].h])
        
        #print(y - x)

    
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

