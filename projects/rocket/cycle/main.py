import itertools
import sys
import io
import contextlib

import scipy.optimize
from CoolProp.CoolProp import PropsSI
import numpy as np
import matplotlib.pyplot as plt

from propellants import *
from point import *
from components import *
from cycle import *

def breakpoint(): import pdb; pdb.set_trace();



def test(c, s, X):
    
    def _f(x):
        setattr(c, s, x)
        c.solve()
        y = c.power_frac(), c.pump.power()
        print(x, y)
        return y

    y = [_f(x) for x in X]

    return y

X = np.linspace(0.01, 0.2, 10)
Y = test(c1, '_bypass', X)

print(Y)

power_frac, pump_power = list(zip(*Y))

fig, axs = plt.subplots(1, 2)

ax = axs[0]
ax.plot(X, power_frac)

ax = axs[1]
ax.plot(X, pump_power)

plt.show()






