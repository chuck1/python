import math
import numpy as np
import matplotlib.pyplot as plt


g = 10.
G = 6.7e-11
M = 1e6

p = math.sqrt(4. * G * M * g)

# calc

t = np.linspace(0., 2. * math.pi, 100)

sint = np.sin(t)

b = 2. * g * sint

a = np.sqrt(p**2. - 2. * b * G * M)


#r = (p - a) / b

#x = r * np.cos(t)
#z = r * sint

#x = (p - a) / (2. * g * np.tan(t))
z = (p - a) / (2. * g)

plt.figure()
plt.plot(t,z)

#plt.figure()
#plt.plot(x,z)

plt.show()




