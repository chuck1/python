from CoolProp.CoolProp import PropsSI
import itertools

from .point import *

class Pump:
    def __init__(self, p0, p1, e=0.8):
        self.p0 = p0
        self.p1 = p1

        equal([p0, p1], 'm')
         
        def _h(p1):
            p1.h_s = PropsSI("H", "P", p1.p, "S", p0.s, p1.f)
            return (p1.h_s - p0.h + p0.h * e) / e

        p1._functions['h'].append(_h)

    def power(self):
        return flow_power(self.p0, self.p1)

def _turbine_h(p, p0, p1, e):
    assert p is p1
    assert p is not p0
    try:
        h_1s = PropsSI("H", "P", p1.p, "S", p0.s, p1.f)
        h_1 = p0.h - e * p0.h + e * h_1s
        return h_1
    except Exception as ex:
        print(ex)
        raise

class Turbine:
    def __init__(self, p0, p1, e):
        self.p0 = p0
        self.p1 = p1

        equal([p0, p1], 'm')

        p1._functions['h'].append(lambda p: _turbine_h(p, p0, p1, e))

    def power(self):
        return -flow_power(self.p0, self.p1)

class Heat(PropertyClass):

    q = PointProperty('q')
    
    def __init__(self, p0, p1):
        super(Heat, self).__init__()
        
        equal([p0, p1], 'm')
        equal([p0, p1], 'p')
        p1._functions['h'].append(lambda p: p0.h + self.q * p0.m)

        self._functions['q'] = [
                lambda c: (p1.h - p0.h) * p0.m,
                ]

    def clear(self):
        super(Heat, self).clear('q')

def flow_power(p0, p1):
    p0.m
    p0.h
    p1.p
    p1.h
    return p0.m * (p1.h - p0.h)

class Mix:
    def __init__(self, p0, p1, p2):
        equal([p0, p1, p2], 'p')

        p2._functions['m'].append(lambda p: p0.m + p1.m)
        p0._functions['m'].append(lambda p: p2.m - p1.m)
        p1._functions['m'].append(lambda p: p2.m - p0.m)

        p2._functions['h'].append(lambda p: (p0.h * p0.m + p1.h * p1.m) / p2.m)

def equal1(p0, p1, s):
        assert p0 is not p1
        
        l0 = p0._functions[s]
        l1 = p1._functions[s]

        assert l0 is not l1

        p0._functions[s].append(lambda p: _f(p, p0, p1, s))

def equal(pts, s):
    for i, j in itertools.permutations(range(len(pts)), 2):
        p0 = pts[i]
        p1 = pts[j]
        
        equal1(p0, p1, s)


def _f(p, p0, p1, s):
    #print(f'{p}.{s} = {p1}.{s}')
    assert p is p0
    assert p is not p1
    return getattr(p1, s)

def _split_f0(p, p0, p1, func):
    f = func()
    m0 = p1.m / f
    assert p1.m > 0
    assert m0 > 0
    return m0

def _split_f1(p, p0, p2, func):
    f = func()
    m0 = p2.m / (1 - f)
    assert p2.m > 0
    assert m0 > 0
    return m0

def _split_f2(p, p0, func):
    f = func()
    m1 = p0.m * f
    assert m1 > 0
    return m1

def _split_f3(p, p0, func):
    f = func()
    assert f > 0
    assert (1 - f) > 0
    m2 = p0.m * (1 - f)
    assert m2 > 0
    return m2


class Split:
    def __init__(self, p0, p1, p2, f):
        
        p0._functions['m'].append(lambda p: _split_f0(p, p0, p1, f))
        p0._functions['m'].append(lambda p: _split_f1(p, p0, p2, f))

        p1._functions['m'].append(lambda p: _split_f2(p, p0, f))
        p2._functions['m'].append(lambda p: _split_f3(p, p0, f))
        
        equal([p0, p1, p2], 'p')
        equal([p0, p1, p2], 'T')
        equal([p0, p1, p2], 'h')
        equal([p0, p1, p2], 's')


