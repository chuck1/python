import matplotlib.pyplot as plt
import math
import numpy as np

import theory
from rocket import *

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

class StageSimData:
    def __init__(self, stage, n):
        self.stage = stage

        self.mass_prop = np.zeros(n)
        self.mass_prop[0] = stage.mass_prop

        self.active = False

    def mass(self, i):
        return self.stage.m_dry + self.mass_prop[i]
    
    @property
    def mdot(self):
        if self.active: return self.stage.mdot
        return 0

    @property
    def thrust(self):
        if self.active: return self.stage.thrust
        return 0

    def activate(self):
        self.active = True
        for s in self.stage.co_staged:
            s.sim.active = True

def battery_capacity_mAh(e, V):
    return e / V / (60*60) * 1000

class Stage:
    def __init__(self, m_wet, m_dry, D_drag, engines, co_staged=[]):
        self.m_wet = m_wet
        self.m_dry = m_dry
        self.engines = engines
        self.A_drag = D_drag**2 / 4 * math.pi
        self.co_staged = co_staged

    def init_sim(self, n):

        self.sim = StageSimData(self, n)

        for e in self.engines:
            e.init_sim(n)

    def print_info(self):
 
        pump_energy_o = sum(e.pump_power_o for e in self.engines) * self.sim.t_off
        pump_energy_f = sum(e.pump_power_f for e in self.engines) * self.sim.t_off
        
        e = pump_energy_o + pump_energy_f
        p = sum(e.pump_power_o for e in self.engines) + sum(e.pump_power_f for e in self.engines)
        

        battery_pot = 3.7*4
        battery_current = p / battery_pot
        battery_capacity = battery_capacity_mAh(e, battery_pot)
        battery_discharge_rating = battery_current / (battery_capacity / 1000)
       
        print(f't_off                 {self.sim.t_off:8.1f} s')
        print(f'pump energy o         {pump_energy_o / 1000:8.1f} kJ')
        print(f'battery potential {battery_pot:8.1f} V')
        print(f'battery current   {battery_current:8.1f} A')
        print(f'battery capacity  {battery_capacity:8.1f} mAh')
        print(f'battery c         {battery_discharge_rating:8.1f} C')


        for e in self.engines:
            print('engine:')
            e.print_info()

    @property
    def isp(self):
        return self.engines[0].isp

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


mag = np.linalg.norm

def alt(x):
    r = mag(x)
    return r - theory.radius_earth


def simulate(r):
    t1 = 800
    dt = 0.05
    n = int(t1 // dt) + 1
    T = np.linspace(0, t1, n)
    a_para = np.zeros(n)
    A = np.zeros((n,2))
    V = np.zeros((n,2))
    X = np.zeros((n,2))
    X[0,1] = theory.radius_earth + 0e3
    TR = np.zeros(n)
    DR = np.zeros(n)
    mass = np.zeros(n)

    for s in r.stages:
        s.init_sim(n)

    stages = list(r.stages)
    stages_drag = list(r.stages)
    
    mass[0] = r.mass_wet

    stage[0].activate()

    #mass_prop = [s.mass_prop for s in stages]

    for i in range(1, n):

        thrust = sum(s.sim.thrust for s in stages)

        speed0 = mag(V[i-1])

        drag = sum(s.drag(speed0, alt(X[i-1])) for s in stages_drag)
        
        if speed0 == 0:
            V_dir = np.array([.08, 1])
            V_dir /= mag(V_dir)
        else:
            V_dir = V[i-1] / speed0

        Drag = -V_dir * drag

        Thrust = V_dir * thrust

        TR[i] = thrust
        DR[i] = drag
        
        vec_grav = -X[i-1] / mag(X[i-1]) * theory.grav(mag(X[i-1]))

        A[i] = (Thrust + Drag) / mass[i-1] + vec_grav

        if np.any(np.isnan(A[i])):
            print(Thrust)
            print(Drag)
            print(vec_grav)
            breakpoint()
        
        a_para[i] = np.dot(A[i], V_dir)

        V[i] = V[i-1] + A[i] * dt

        X[i] = X[i-1] + V[i] * dt

        if np.any(np.isnan(X[i])):
            breakpoint()

        if alt(X[i]) < 0:
            print(X[i])
            break

        #if math.isnan(A[i]): breakpoint()

        for s in stages:
            for e in s.engines:
                e.sim.mdot[i] = e.mdot
                e.sim.mdot_fuel[i] = e.mdot_fuel
                e.sim.mdot_oxidizer[i] = e.mdot_oxidizer

        mdot = sum(s.sim.mdot for s in stages)
        
        #print(f'{mag(V[i]):8.2f} {mass[i-1]} {mass_prop}')
        
        if stages:

            stages[0].sim.mass_prop[i] = stages[0].sim.mass_prop[i-1] - mdot * dt

            for s in stages[1:]:
                s.sim.mass_prop[i] = s.sim.mass_prop[i-1]

            if stages[0].sim.mass_prop[i] < 0:

                stages[0].sim.t_off = T[i]

                stages.pop(0)

                if len(stages_drag) > 1:
                    stages_drag.pop(0)

        mass[i] = sum(s.sim.mass(i) for s in stages_drag)

    theta = np.arctan2(X[:i,1], X[:i,0])
    
    fig, axs = plt.subplots(2, 3)

    axs[0, 0].plot(T, np.linalg.norm(V, axis=1))
    axs[0, 0].plot([T[0], T[-1]], [343, 343])
    axs[0, 0].set_ylabel('speed (m/s)')

    axs[0, 1].plot(T[:i], np.linalg.norm(X[:i], axis=1) - theory.radius_earth)
    axs[0, 1].set_ylabel('altitude (m)')

    axs[0, 2].plot(T, TR)
    axs[0, 2].plot(T, DR)

    axs[1, 0].plot(T, a_para / 9.81, label='flight direction')
    axs[1, 0].set_ylabel('accel (g)')
    axs[1, 0].legend()

    def plot_flow(ax):
        for s in r.stages:
            for e in s.engines:
                ax.plot(T, e.sim.mdot_fuel / e.density_f * 1000, label='F')
                ax.plot(T, e.sim.mdot_oxidizer / e.density_o * 1000, label='O')
        ax.legend()
        ax.set_ylabel('flow rate (L/s)')

    def plot_mass(ax):
        ax.plot(T[:i], mass[:i])
        ax.set_ylabel('mass (kg)')

    #plot_flow(axs[1, 1])
    plot_mass(axs[1, 1])

    fig, ax = plt.subplots(1, 1)
    ax.plot(X[:i,0], X[:i,1])
    ax.plot(theory.radius_earth * np.cos(theta), theory.radius_earth * np.sin(theta))
    ax.axis('equal')
    plt.show()
    
def plot_mach_factor():
    M = np.linspace(0, 10, 1000)
    f = [mach_factor(M1) for M1 in M]
    plt.plot(M, f)
    plt.show()

def test1():
    r = Rocket()
    s1 = Stage(80, 20, 0.200, [Engine(0.005), Engine(0.005)], co_staged=[s2])
    s2 = Stage(40, 10, 0.100, [Engine(0.005)])
    s2 = Stage(20, 10, 0.100, [Engine(0.005)])
    
    r.stages = [s1, s2, s3]
    #r.stages = [s2]
    
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


#plot_mach_factor()

r = test1()

simulate(r)

r.print_info()

#radio = Radio()
#print radio.power(400e3, 5e-6)




