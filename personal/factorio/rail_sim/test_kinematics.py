import numpy as np
import matplotlib.pyplot as plt

# given

def f(T, X, v0, v1):
    
    # v1 limits
    
    # choose v1
    
    
    # calculate a
    
    a = -(v1 - v0)**2 / (X - v1 * T)
    
    print("a", a)
    
    # additional calcs
    
    # T1 will be negative if
    # 2 * (v1 - v0) / a > T 
    
    # so lets enforce
    # 2 * (v1 - v0) / a <= T 
    # 2 * (v1 - v0) / a <= T 
    
    
    T1 = T - 2 * (v1 - v0) / a
    T0 = (T - T1) / 2
    
    X1 = v1 * T1
    X0 = (X - X1) / 2
    
    # plot
    
    t = np.linspace(0, T0)
    x = v0 * t + 0.5 * a * t**2
    
    plt.plot(t, x)
    
    t = np.linspace(0, T1)
    x = v1 * t
    
    plt.plot(t + T0, x + X0)
    
    t = np.linspace(0, T0)
    x = v1 * t - 0.5 * a * t**2
    
    plt.plot(t + T0 + T1, x + X0 + X1)

def f2(T, X, v0):
    
    a = (X - v0 * T) / (T**2 / 4)
    
    v1 = v0 + a * T / 2

    print("a", a)
    
    # plot
    
    t = np.linspace(0, T / 2)
    x = v0 * t + 0.5 * a * t**2
    
    plt.plot(t, x)
    
    t = np.linspace(0, T / 2)
    x = v1 * t - 0.5 * a * t**2
    
    plt.plot(t + T / 2, x + X / 2)

f(20, 10, 1, 0.4)
f2(20, 10, 1)

plt.show()
    
