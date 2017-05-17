import math
import numpy as np
import pylab as pl
import random

# cumulative error
e_x = 0
e_v = 0

# measurement error
# 16 bit ADC
# most sensitive full scale is +- 2 g
# so error is
digital_range = 2**16
meas_range = 4*9.81
meas_err = meas_range / digital_range
print 'digital_range',digital_range
print 'measurement range',meas_range
print 'measurement error',meas_err

def kinematics(f, t):
	o = 2.0 * math.pi * f
	X = np.cos(o * t)
	V = -o * np.sin(o * t)
	A = -o**2 * np.cos(o * t)
	
	return X,V,A

def kinematics2(f, t):
	a = 1.0
	X = 0.5 * np.square(t) * a
	V = t * a
	A = t * 0 + a
	
	return X,V,A

def error_series(t):
	#n = len(t)
	
	e = np.sin(2.0 * math.pi * 400.0 * t)
	
	return e
	
	
def run(ax, f_sam, f, t_f):
	
	f_sam = 200.0
	h = 1.0 / f_sam
	
	n = int(t_f / h)
	
	x = np.zeros(n)
	v = np.zeros(n)

	t = np.arange(n) * h
	
	X,V,A = kinematics(f, t)
	
	# position and velocity are accurate at t=0
	x[0] = X[0]
	v[0] = V[0]
	
	#e[0] = random.uniform(-1,1) * meas_err
	e = error_series(t)
	
	for i in range(1,n):
		
		# measurement error
		# worst case
		A_a = A[i] + e[i]
		A_b = A[i-1] + e[i-1]
		
		v[i] = v[i-1] + h/2.0 * (A_a + A_b)
		x[i] = x[i-1] + h/2.0 * (v[i] + v[i-1])
	
	#print np.mean(e)

	ax.plot(t,x-X)
	
	

fig = pl.figure()
ax = fig.add_subplot(111)

#run(ax, 200.0,  5.0)
#run(ax, 200.0, 10.0)
#run(ax, 200.0, 20.0)
#run(ax, 200.0, 40.0)

#run(ax,  50.0,  5.0)
run(ax, f_sam = 100.0, f = 10.0, t_f = 100.0)
#run(ax, 200.0, 20.0)
#run(ax, 400.0, 40.0)


ax.set_ylabel('x error')
ax.set_xlabel('t')
pl.show()



