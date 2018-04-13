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
    def __init__(self, n):
        pass

def battery_capacity_mAh(e, V):
    return e / V / (60*60) * 1000

class Stage:
    def __init__(self, m_wet, m_dry, A_drag, engines):
        self.m_wet = m_wet
        self.m_dry = m_dry
        self.engines = engines
        self.A_drag = A_drag

       
    def init_sim(self, n):

        self.sim = StageSimData(n)

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

class EngineSimData:
    def __init__(self, n):
        self.mdot = np.zeros(n)
        self.mdot_fuel = np.zeros(n)
        self.mdot_oxidizer = np.zeros(n)

class Engine:
    def __init__(self, D_throat):
        self.T_c = 3676 # K
        self.p_c = 6.89e6 # Pa
        self.v_e = 2941 # m/s
        
        self.D_throat = D_throat
        self.A_throat = self.D_throat**2 / 4 * math.pi

        self.o_f_ratio = 2.56

        self.density_o = 1141 # kg/m3
        self.density_f = 810 # kg/m3

        self.p_tank_o = 101325 # Pa
        self.p_tank_f = 101325 # Pa

    def print_info(self):
        print(f'pump power o {self.pump_power_o:8.1f} W')
        print(f'pump power f {self.pump_power_f:8.1f} W')

    @property
    def pump_power_o(self):
        p = self.p_c - self.p_tank_o
        V = self.mdot_oxidizer / self.density_o
        return p * V

    @property
    def pump_power_f(self):
        p = self.p_c - self.p_tank_f
        V = self.mdot_fuel / self.density_f
        return p * V

    @property
    def mdot_fuel(self):
        return self.mdot * (1 / (1 + self.o_f_ratio))

    @property
    def mdot_oxidizer(self):
        return self.mdot * (1 / (1 + 1 / self.o_f_ratio))

    @property
    def mdot(self):
        gamma = 1.2
        return theory.choked_flow(self.A_throat, self.p_c, self.T_c, gamma)

    @property
    def thrust(self):
        return theory.thrust(self.mdot, self.v_e, 0, 0, 0)

    def init_sim(self, n):
        self.sim = EngineSimData(n)

   
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

    for s in r.stages:
        s.init_sim(n)

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

        for s in stages:
            for e in s.engines:
                e.sim.mdot[i] = e.mdot
                e.sim.mdot_fuel[i] = e.mdot_fuel
                e.sim.mdot_oxidizer[i] = e.mdot_oxidizer

        mdot = sum(s.mdot for s in stages)
        
        #print(f'{V[i]:8.2f} {mass_prop}')

        if mass_prop:
            mass_prop[0] -= mdot * dt

            if mass_prop[0] < 0:

                stages[0].sim.t_off = T[i]

                stages.pop(0)
                mass_prop.pop(0)

                if len(stages_drag) > 1:
                    stages_drag.pop(0)
   
    fig = plt.figure()
    ax = fig.add_subplot(231)
    ax.plot(T, V)
    ax.plot([T[0], T[-1]], [343, 343])
    ax.set_ylabel('speed (m/s)')

    ax = fig.add_subplot(232)
    ax.plot(T, X)
    ax.set_ylabel('altitude (m)')

    ax = fig.add_subplot(233)
    ax.plot(T, TR)
    ax.plot(T, DR)

    ax = fig.add_subplot(234)
    ax.plot(T, A / 9.81)
    ax.set_ylabel('accel (g)')

    ax = fig.add_subplot(235)
    for s in r.stages:
        for e in s.engines:
            ax.plot(T, e.sim.mdot_fuel)
    ax.set_ylabel('mdot F (kg/s)')

    ax = fig.add_subplot(236)
    for s in r.stages:
        for e in s.engines:
            ax.plot(T, e.sim.mdot_oxidizer / e.density_o * 1000)
    ax.set_ylabel('O flow rate (L/s)')

    plt.show()
    
def plot_mach_factor():
    M = np.linspace(0, 10, 1000)
    f = [mach_factor(M1) for M1 in M]
    plt.plot(M, f)
    plt.show()

def test1():
    r = Rocket()
    s1 = Stage(40, 4, 0.01570, [Engine(0.005), Engine(0.005)])
    s2 = Stage(40, 8, 0.00785, [Engine(0.005)])
    
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


#plot_mach_factor()

r = test1()

simulate(r)

r.print_info()

#radio = Radio()
#print radio.power(400e3, 5e-6)




