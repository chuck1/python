import copy
import matplotlib.pyplot as plt
import math
import numpy as np

from . import theory
from .rocket import *
from .engine import *
from .util import *

def breakpoint(): import pdb; pdb.set_trace();

class StageSimData:
    def __init__(self, stage, sim):
        self.stage = stage
        self.sim = sim

        self.mass_prop = np.zeros(self.sim.n)
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

class Stage:
    def __init__(self, m_wet=0, m_dry=0, D_drag=0, engines=[], co_staged=[], prop=None):
        self.m_wet = m_wet
        self.m_dry = m_dry
        self.engines = [copy.copy(e) for e in engines]
        self.A_drag = D_drag**2 / 4 * math.pi
        self.co_staged = co_staged
        self.prop = prop
        
        for e in self.engines:
            e.stage = self

    def activate(self, i):
        self.sim.active = True
        for s in self.co_staged:
            s.sim.active = True

    def init_sim(self, sim):

        self.sim = StageSimData(self, sim)

        for e in self.engines:
            e.init_sim(sim.n)

    def print_info(self, indent=''):
 
        pump_energy_o = sum(e.pump_power_o for e in self.engines) * self.sim.t_off
        pump_energy_f = sum(e.pump_power_f for e in self.engines) * self.sim.t_off
        
        e = pump_energy_o + pump_energy_f
        p = sum(e.pump_power_o for e in self.engines) + sum(e.pump_power_f for e in self.engines)
        

        battery_pot = 3.7*4
        battery_current = p / battery_pot
        battery_capacity = battery_capacity_mAh(e, battery_pot)
        battery_discharge_rating = battery_current / (battery_capacity / 1000)
       
        print(indent + f't_off                 {self.sim.t_off:8.1f} s')
        print(indent + f'pump energy o         {pump_energy_o / 1000:8.1f} kJ')
        print(indent + f'battery potential     {battery_pot:8.1f} V')
        print(indent + f'battery current       {battery_current:8.1f} A')
        print(indent + f'battery capacity      {battery_capacity:8.1f} mAh')
        print(indent + f'battery c             {battery_discharge_rating:8.1f} C')


        for e in self.engines:
            print(indent + 'engine:')
            e.print_info(indent + '  ')

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



