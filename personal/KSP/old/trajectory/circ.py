from pylab import plot, show, figure
import numpy as np
import math

def circ(xc, yc, r, t):
	
	x = xc + r * np.cos(t)
	y = yc + r * np.sin(t)
	
	return x, y

def ell(xc, yc, a, b, t):

	x = xc + a * np.cos(t)
	y = yc + b * np.sin(t)

	return x, y

def circ2(x, y, xc, yc, r):
	
	return ((x - xc)**2 + (y - yc)**2 - r**2)

'''
t = np.linspace(0, 2 * math.pi, 100)

fig = figure()
ax = fig.add_subplot(111, aspect='equal')

x, y = circ(0, 0, 1, t)

ax.plot(x, y, '-o')

x, y = ell(0, 0, 2, 0.5, t)

ax.plot(x, y, '-o')

show()
'''

#xc + r * math.cos(s) - xe - a * math.cos(t) = 0
#yc + r * math.sin(s) - ye - b * math.sin(t) = 0

def cir_ell(xc, yc, xe, ye, r, a, b):
	
	t = 0.5
	s = 0.5
	
	it = 0

	while True:
		
		c = xc + r * math.cos(s) - xe
		d = xe + a * math.cos(s) - xc

		try:
			t = math.acos(c) / a
		except:
			print "c =",c
			break
	
		try:
			s = math.acos(d) / r
		except:
			print "d =",d
			break


	
		plot(t,'o')
		plot(s,'o')
		
		if it > 100:
			break
		it += 1
	
	show()

def func(c, e, t):
	x, y = e(t)
	f = c(x, y)
	return f
	
def circ_fun(xc, yc, r):
	return lambda x, y: ((x - xc)**2 + (y - yc)**2 - r**2)

def ell_fun(xe, ye, a, b):
	e = lambda t: (xe + a * np.cos(t), ye + b * np.sin(t))
	return e

def zero(t0, t1, F, depth=0):
	
	t = np.linspace(t0, t1, 100)
	
	f = F(t)
	
	s = math.copysign(1, f[0])
	for i in range(len(f)):
		ns = math.copysign(1, f[i])
		if s != ns:
			
			if depth > 0:
				zero(t[i-1], t[i], F, depth - 1)
			else:
				print t[i-1],t[i]
			
		s = ns
	
	return

#cir_ell(0, 0, 0, 0, 1, 2, 0.5)

c = circ_fun(0, 0, 1)
e = ell_fun(0, 0, 2, 0.5)

t = np.linspace(0, 2 * math.pi, 100)

f = func(c, e, t)

plot(t, f)
show()

F = lambda t: func(c, e, t)

zero(0, 2 * math.pi, F, 2)


