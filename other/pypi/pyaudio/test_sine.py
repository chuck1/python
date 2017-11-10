import math
import matplotlib.pyplot as plt
import numpy as np

def sine_wave(t, f):
    return np.sin(2 * math.pi / f * t)

def pitch_increase_linear(t, x1, y1):
    a = (y1 - 1) / 2 / x1
    b = x1 / (y1 - 1)
    return a * np.power(t + b, 2)

def test():
    
    t = np.linspace(0, 10, 1000)
    
    t2 = np.power(t, 2)

    t2 = pitch_increase_linear(t, 10, 2)
    
    plt.plot(t, t2)
    plt.show()

    y = sine_wave(t2, 1)
    
    plt.plot(t,y)
    plt.show()

    


test()


