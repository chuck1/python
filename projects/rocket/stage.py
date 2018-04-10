import math
import numpy as np

class Radio(object):
    def power(self, d, E):
        #E = 1e-6

        # E = sqrt(30 * P) / d
        # E * d = sqrt(30 * P)
        # (E * d)**2 = 30 * P
        # P = (E * d)**2 / 30
        P = (E * d)**2 / 30.0

        return P

class Rocket:
    stages = []

    @property
    def mass_wet(self):
        return sum([s.m_wet for s in stages])

    def deltav(self):
        stages = list(self.stages)

        m_wet = sum([s.m_wet for s in stages])

        dv = 0

        while stages:
            s = stages.pop(0)

            m_dry = m_wet - s.mass_prop
            
            dv_temp = s.isp * 9.81 * math.log(m_wet / m_dry)

            dv += dv_temp

            if 0:
                print("m_wet  ", m_wet)
                print("m_dry  ", m_dry)
                print("log    ", math.log(m_wet / m_dry))
                print("log    ", m_wet / m_dry)
                print("isp    ", s.isp)
            
            print("dv_temp", dv_temp)

            m_wet -= s.m_wet

        return dv

class Stage:
    def __init__(self, m_wet, m_dry, isp):
        self.m_wet = m_wet
        self.m_dry = m_dry
        self.isp = isp

    @property
    def mass_prop(self):
        return self.m_wet - self.m_dry

def test1():
    r = Rocket()
    s1 = Stage(80, 4, 300)
    s2 = Stage(30, 2, 300)
    
    r.stages = [s1, s2]
    
    print('delta v total:', r.deltav())
    
    return r

def test2():
    r = Rocket()
    s1 = Stage()
    
    s1.Isp = 200.
    s1.m_wet = 20.0
    s1.m_dry = 10.0
    
    r.stages = [s1]
    
    print(r.deltav())
    
def simulate(r):
    n = 1001
    t1 = 100
    dt = t1 / (n - 1)
    T = np.linspace(0, t1, n)
    V = np.zeros(n)
    
    stages = list(r.stages)
    mass = r.mass_wet

    for i in range(1, n):
        a = thrust / mass
        V[i] = V[i-1] + a * dt
    
    


r = test1()

simulate(r)

#radio = Radio()
#print radio.power(400e3, 5e-6)


