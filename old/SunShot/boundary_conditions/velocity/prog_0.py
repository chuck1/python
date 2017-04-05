import sys
sys.path.append('/nfs/stak/students/r/rymalc/Documents/python')
import matplotlib.pyplot as plt
import Mod

import numpy as np

def prof_exp(x,n):
	ratio1 = ( n + 2.0 ) / n
	y = ratio1 * ( 1 - np.power(x,n) )
	return y



x = Mod.frange(0,0.9999,0.001)
x = np.append(x,1.0)
#print "x",x

# ratio  = umax/um
# ratio2 = ut/umax
# y      = u/um

#-----------------------------------------------
# handbook of single-phase convective heat transfer (hspcht) eq 4.41
n = 6.6

ratio1 = (n+1)*(2.0*n+1)/(2.0*n*n)
print "ratio1 %f" % ratio1

p = 1.0/n
#print "p %f" % p

y3 = ratio1 * np.power( 1.0-x, p )
#print "y2",y2

# hspcht eq 4.42
#ratio1 = ??
ratio2 = 0.05 #??

y4 = ratio1 * ( 1 - ratio2 * 2.5 * np.log( 1.0/(1.0-x) ) )

# hspcht
#ratio1 = ??
ratio2 = 0.05 #??

y5 = ratio1 * ( 1 + ratio2 * 2.5 * ( np.log( 1.0 - np.sqrt(x) ) + np.sqrt(x) ) )





plt.plot(x,y3,x,y4,x,y5)
plt.axis([0, 1, 0, 2])
plt.show()



