import matplotlib.pyplot as plt
import math
import numpy as np

import theory

def breakpoint(): import pdb; pdb.set_trace();

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
        return sum([s.m_wet for s in self.stages])

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

def mach_factor(M):
    if M < 0.8:
        return 1
    elif M < 1.2:
        return 3
    else:
        x0 = 1.2
        y0 = 3
        a = - math.log(0.5 / y0) / (10 - x0)
        return y0 * math.exp(-a * (M - x0))

class Stage:
    def __init__(self, m_wet, m_dry, A_drag, engines):
        self.m_wet = m_wet
        self.m_dry = m_dry
        self.engines = engines
        self.A_drag = A_drag
        

    @property
    def isp(self):
        return 0

    @property
    def mass_prop(self):
        return self.m_wet - self.m_dry

    @property
    def mdot(self):
        return sum(e.mdot for e in self.engines)

    @property
    def thrust(self):
        return sum(e.thrust for e in self.engines)

    def Cd(self, v):
        return 0.25 * mach_factor(v / 343)

    def drag(self, v, h):
        """
        v speed
        h altitude
        """
        Cd = 0.25
        
        # air density
        L = 0.0065 # K/m
        M = 0.0289644 # kg/mol
        g = 9.81
        T0 = 288.15
        p0 = 101325
        R = theory.R
        T = T0 - L*h
        a = 1 - L*h/T0

        if a < 0:
            return 0

        p = p0 * (a)**(g*M/R/L)
        rho = p * M / R / T
        
        Cd = self.Cd(v)

        drag = Cd * rho * v**2 / 2 * self.A_drag
        
        if math.isnan(drag):
            breakpoint()

        return drag

class Engine:
    def __init__(self):
        self.T_c = 3676
        self.p_c = 6.89e6
        self.v_e = 2941
        
        self.D_throat = 0.01
        self.A_throat = self.D_throat**2 / 4 * math.pi

    @property
    def mdot(self):
        gamma = 1.2
        return theory.choked_flow(self.A_throat, self.p_c, self.T_c, gamma)

    @property
    def thrust(self):
        return theory.thrust(self.mdot, self.v_e, 0, 0, 0)

def test1():
    r = Rocket()
    s1 = Stage(40, 4, 0.01570, [Engine(), Engine()])
    s2 = Stage(20, 4, 0.00785, [Engine()])
    
    #r.stages = [s1, s2]
    r.stages = [s2]
    
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
    t1 = 500
    dt = 0.1
    n = int(t1 // dt) + 1
    T = np.linspace(0, t1, n)
    A = np.zeros(n)
    V = np.zeros(n)
    X = np.zeros(n)
    TR = np.zeros(n)
    DR = np.zeros(n)
    
    stages = list(r.stages)
    stages_drag = list(r.stages)
    mass = r.mass_wet
    
    mass_prop = [s.mass_prop for s in stages]

    for i in range(1, n):

        thrust = sum(s.thrust for s in stages)
        drag = sum(s.drag(V[i-1], X[i-1]) for s in stages_drag)
        
        drag = math.copysign(drag, V[i-1])

        TR[i] = thrust
        DR[i] = drag

        A[i] = (thrust - drag) / mass - 9.81

        V[i] = V[i-1] + A[i] * dt
        X[i] = X[i-1] + V[i] * dt
        
        if X[i] < 0:
            break

        if math.isnan(A[i]): breakpoint()

        mdot = sum(s.mdot for s in stages)
        
        print(f'{V[i]:8.2f} {mass_prop}')

        if mass_prop:
            mass_prop[0] -= mdot * dt

            if mass_prop[0] < 0:
                stages.pop(0)
                mass_prop.pop(0)

                if len(stages_drag) > 1:
                    stages_drag.pop(0)
   
    fig = plt.figure()
    ax = fig.add_subplot(141)
    ax.plot(T, V)
    ax.plot([T[0], T[-1]], [343, 343])
    ax.set_ylabel('speed (m/s)')

    ax = fig.add_subplot(142)
    ax.plot(T, X)
    ax.set_ylabel('altitude (m)')

    ax = fig.add_subplot(143)
    ax.plot(T, TR)
    ax.plot(T, DR)

    ax = fig.add_subplot(144)
    ax.plot(T, A / 9.81)
    ax.set_ylabel('accel (g)')

    plt.show()
    

def plot_mach_factor():
    M = np.linspace(0, 10, 1000)
    f = [mach_factor(M1) for M1 in M]
    plt.plot(M, f)
    plt.show()

#plot_mach_factor()

r = test1()

simulate(r)

#radio = Radio()
#print radio.power(400e3, 5e-6)


