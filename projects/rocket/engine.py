import matplotlib.pyplot as plt
import math
import numpy as np

import theory
from rocket import *

def breakpoint(): import pdb; pdb.set_trace();

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

  
