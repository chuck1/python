import math
import numpy as np
from matplotlib import pyplot as plt

Do = np.array([1,   2,    4,   8,   20])
Ko = np.array([0.5, 0.39, 0.3, 0.26, 0.21]) 

Do = Do * 0.0254

D = np.log(Do)
K = np.log(Ko)


f = np.polyfit(D,K,1)

#plt.plot(D,K,'o')
#plt.show()

k = lambda d: math.exp(f[1]) * d**f[0]

print k(0.0254)
print k(4e-4)

d = np.logspace(-5,0)
plt.loglog(d,k(d))
plt.plot(Do,Ko,'o')
plt.show()



