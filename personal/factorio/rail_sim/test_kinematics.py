import numpy as np
import matplotlib.pyplot as plt

from conductor.util import *

# given

def plot(ax, t0, t1, x0, v0, a0):
    t = np.linspace(t0, t1)
    x = x0 + v0 * (t - t0) + a0 / 2 * (t - t0)**2
    ax.plot(t, x)

T = 20
X = 10
v0 = 1

fig = plt.figure()
ax = fig.add_subplot(111)

# 1

v1 = 0.4

a, T0, T1, X0, X1 = acc_dec_1(T, X, v0, v1)

plot(ax, 0, T0, 0, v0, a)
plot(ax, T0, T0 + T1, X0, v1, 0)
plot(ax, T0 + T1, T, X0 + X1, v1, -a)

# 2

a, v1 = acc_dec_2(T, X, v0)

plot(ax, 0, T / 2, 0, v0, a)
plot(ax, T / 2, T, X / 2, v1, -a)

# 3

a0 = -0.25
a2 = 0.125

T0, T1, X0, X1, v1 = acc_dec_3(T, X, v0, a0, a2)

plot(ax, 0, T0, 0, v0, a0)
plot(ax, T0, T0 + T1, X0, v1, 0)
plot(ax, T0 + T1, T, X0 + X1, v1, a2)


plt.show()
    
