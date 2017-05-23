from pylab import show, plot

from sympy import *

def circ(xc, yc, r, t):
	x = xc + r * (1 - t**2) / (1 + t**2)
	y = yc + r * (2 * t) / (1 + t**2)
	return x,y

def coeff():

	a, b, c, d, f, g, r, t = symbols('a, b, c, d, f, g, r, t')
	
	x = f + r * (1 - t**2) / (1 + t**2)
	y = g + r * (2 * t) / (1 + t**2)

	expr = (x - c)**2 / a**2 + (y - d)**2 / b**2 - 1
	
	expr = expand(expr)
	expr = expr * (t**2 + 1)**2 * a**2 * b**2
	expr = cancel(expr)
	expr = collect(expr, t)
	
	#pprint(expr)
	
	#print srepr(expr)
	
	#print expr.args
	
	
	c4 = expr.coeff(t**4)
	c3 = expr.coeff(t**3)
	c2 = expr.coeff(t**2)
	c1 = expr.coeff(t**1)
	c0 = expr - c4 * t**4 - c3 * t**3 - c2 * t**2 - c1 * t**1
	
	l0 = lambdify((a, b, c, d, f, g, r), c0)
	l1 = lambdify((a, b, c, d, f, g, r), c1)
	l2 = lambdify((a, b, c, d, f, g, r), c2)
	l3 = lambdify((a, b, c, d, f, g, r), c3)
	l4 = lambdify((a, b, c, d, f, g, r), c4)
	
	return l0, l1, l2, l3, l4

def cir_ell(xc, yc, xe, ye, a, b, r):
	
	c = xe
	d = ye
	g = xc
	f = yc
	
	l = coeff()
	
	a = l[4](a, b, xe, ye, xc, yc, r)
	b = l[3](a, b, xe, ye, xc, yc, r)
	c = l[2](a, b, xe, ye, xc, yc, r)
	d = l[1](a, b, xe, ye, xc, yc, r)
	f = l[0](a, b, xe, ye, xc, yc, r)
	
	s = solve1()
	
	print a, b, c, d, f

	t = s(a+0j, b+0j, c+0j, d+0j, f+0j)
	
	#print t
	return t

def solve1():
	
	a, b, c, d, f, t = symbols('a b c d f t')
	
	expr = a*t**4 + b*t**3 + c*t**2 + d*t + f
	
	#print expr
	
	s = solve(expr,t)
	
	#print s
	
	#print len(s)
	
	s = lambdify((a, b, c, d, f), s)
	
	#s(co[4], co[3], co[2], co[1], co[0]

	return s

	#print s


xc = 0
yc = 0
r = 0

t = cir_ell(0, 0, 0, 0, 2, 0.5, 1)

x,y = circ(xc, yc, r, t[0])

print x,y

#plot(x,y,'o')
#show()



