import math
import numpy as np
import matplotlib.pyplot as plt

n = 10000

# orbit info
v = np.array([2900,0])

x = np.zeros((n,2))
s = np.zeros(n)
r = np.zeros(n)


x[0,0] = 0
x[0,1] = 800000

# ship info
m = 100
d = 0.2

dt = 0.2

dragMultiplier = 0.008
atmDensityScale = 1.2230948554874

A = dragMultiplier * m

# body info
mu = 3.5316e12
sh = 5000
p0 = 1
R = 600000
ah = 69000

def density(p0,h,a):
	if a < ah:
		p = p0 * math.exp(-a/h)
		rho = atmDensityScale * p
		print rho
	else:
		rho = 0
	return rho

i_stop = n
for i in range(1,n):
	r[i-1] = np.linalg.norm(x[i-1,:])#math.sqrt(np.sum(np.power(x[i-1,:],2)))
	s[i-1] = np.linalg.norm(v)
	
	if r[i-1] < R:
		i_stop = i-1
		break
	
	
	alt = r[i-1] - R
	
	print alt
	
	rho = density(p0,sh,alt)
	FG = -m * mu / math.pow(r[i-1],3) * x[i-1,:]
	FD = -0.5 * rho * s[i-1] * d * A * v

	F = FG + FD
	
	
	
	a = F / m
	
	
	
	v += a * dt
	x[i,:] = x[i-1,:] + v * dt

circle = plt.Circle((0,0),R,color='g')
plt.gca().add_artist(circle)

plt.plot(x[0:i_stop,0],x[0:i_stop,1],'-')
plt.axis('equal')
plt.show()


plt.plot(r[0:i_stop])
plt.show()

plt.plot(s[0:i_stop])
plt.show()

print r

