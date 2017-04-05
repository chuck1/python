import struct
import numpy as np
import matplotlib.pyplot as plt
import sys



for arg in sys.argv: 
    print arg

with open("test.bin", "rb") as f:
	a = np.fromfile(f, float)

print a

x=a[0:5:1]
y=a[5:10:1]

print x
print y

plt.plot(x, y)


plt.show()
