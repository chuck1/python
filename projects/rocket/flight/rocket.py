import matplotlib.pyplot as plt
import math
import numpy as np

from . import theory

def breakpoint(): import pdb; pdb.set_trace();

class Rocket:
    stages = []

    def print_info(self, indent=''):
        for s in self.stages:
            print(indent + 'stage:')
            s.print_info(indent+'  ')

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


