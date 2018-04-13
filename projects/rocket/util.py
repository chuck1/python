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


def battery_capacity_mAh(e, V):
    return e / V / (60*60) * 1000

mag = np.linalg.norm

def alt(x):
    r = mag(x)
    return r - theory.radius_earth


