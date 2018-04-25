from CoolProp.CoolProp import PropsSI
import itertools

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


def _f(p, p0, p1, s):
    #print(f'{p}.{s} = {p1}.{s}')
    assert p is p0
    assert p is not p1
    return getattr(p1, s)

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


