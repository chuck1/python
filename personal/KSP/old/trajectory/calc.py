import numpy as np
import math
import inspect
#import matplotlib.pyplot as plt
from pylab import figure, show, rand, plot
from matplotlib.patches import Ellipse, Circle, Arrow
from matplotlib.lines   import Line2D

# ma mean anomaly
# ta true anomaly
# Ea eccentric anomaly

# R  body radius

# E  eccentricity vector

# r  position vector

# n  ascending node vector

# -c m^2+2 c m x-c x^2-d n^2+2 d n y-d y^2+f^2-2 f x+g^2-2 g y+x^2+y^2 = (r-1) (r+1)


def solve(x, y, gx, gy):
	X = [x]
	Y = [y]
	it = 0
	
	thresh = 1E-6

	while True:
		dx = gx(y) - x
		x += dx
		
		dy = gy(x) - y
		y += dy
		
		X.append(x)
		Y.append(y)
		
		
		
		if math.fabs(dy) < thresh and math.fabs(dx) < thresh:
			break
		if it > 100:
			print "AAAAAAAAAAAAAAAAAAAA!!!!!!!!!"
			raise

		it += 1

	plot(X,'b-o')
	plot(Y,'r-o')
	show()

	return x,y



def two_var_non_lin(a, b, c, d, f):
	gxs = lambda y: b**2 - 4 * a * (c * y**2 + d * y + f)
	
	gx1 = lambda y: (-b + math.sqrt(gxs(y))) / 2 / a
	gx2 = lambda y: (-b - math.sqrt(gxs(y))) / 2 / a
	
	gys = lambda x: d**2 - 4 * c * (a * x**2 + b * x + f)
	
	gy1 = lambda x: (-d + math.sqrt(gys(x))) / 2 / c
	gy2 = lambda x: (-d - math.sqrt(gys(x))) / 2 / c
	
	print a, b, c, d, f

	y0 = 1
	x0 = 1

	x1,y1 = solve(x0, y0, gx1, gy1)
	x2,y2 = solve(x0, y0, gx2, gy1)
	x3,y3 = solve(x0, y0, gx1, gy2)
	x4,y4 = solve(x0, y0, gx2, gy2)


	return x1,x2,x3,x4,y1,y2,y3,y4

def plane_sphere(n, D, p, R):
	a = np.dot(n,p) + D
	b = np.dot(n,n)

	c = p - a/b * n

	d = math.fabs(a) / math.sqrt(b)
	
	r = math.sqrt(R**2 - d**2)

def circle_ellipse(xc,yc,xe,ye,r,a,b):
	c = 1 / a**2
	d = 1 / b**2
	
	x1,x2,x3,x4,y1,y2,y3,y4 = two_var_non_lin(
			1 - c,
			2 * c * xe - 2 * xc,
			1 - d,
			2 * d * ye - 2 * yc,
			xc**2 + yc**2 - c * xe**2 - d * ye**2 - r**2 + 1)

	return [x1,x2,x3,x4],[y1,y2,y3,y4]

def rotate(v,a):
	ca = math.cos(a)
	sa = math.sin(a)
	
	l = v[0]
	m = v[1]
	n = v[2]

	m = np.matrix([
		[l * l * (1 - ca) + 1 * ca, m * l * (1 - ca) - n * sa, n * l * (1 - ca) + m * sa],
		[l * m * (1 - ca) + n * sa, m * m * (1 - ca) + 1 * ca, n * m * (1 - ca) - l * sa],
		[l * n * (1 - ca) - m * sa, m * n * (1 - ca) + l * sa, n * n * (1 - ca) + 1 * ca]])
	
	return m


def orbit_1(body, p, v, t):

	pbody = np.array([[0],[0],[0]])
	if(body.orbit):
		pbody += body.orbit.position_abs(t)
	
	angle = math.tan((p[1] - pbody[1]) / (p[0] - pbody[1]))
	
	V = math.sqrt(np.sum(np.square(v)))
	
	v = rotate([0,0,1], -angle) * v
	
	
	vr = v[0,0]
	vt = v[1,0]
	
	r = math.sqrt(np.sum(np.square(p - pbody)))
	
	a = 1 / (2 / r - V**2 / body.mu)

	l = vt**2 * r**2 / body.mu
	e = math.sqrt(1 - l / a)
	h = math.sqrt(l * body.mu)
	
	ta = math.asin(vr * l / h / e)
	
	rp = a * (1 - e)
	ra = a * (1 + e)
	
	per = rp + body.R
	apo = ra + body.R

	aop = angle - ta
	
	o = Orbit(body, per, apo, 0, aop, 0)
	
	o.ma = o.ta_to_ma(ta) - o.t_to_ma(t)
	
	

	return o
	
	
class Orbit:
	def __init__(self, body, per, apo, inc, aop, ma):
		self.body = body
		self.per = per
		self.apo = apo
		self.inc = inc
		self.aop = aop
		self.ma = ma

		self.rp = per + body.R
		self.ra = apo + body.R
		
		self.a = (self.ra + self.rp)/2
		self.e = (self.ra - self.rp)/(self.ra + self.rp)
		self.b = self.a * math.sqrt(1 - self.e**2)

		temp = np.array([[math.cos(self.aop)], [math.sin(self.aop)], [0]])
		
		self.Eu = temp
		self.E = temp * self.e
		
		self.n = np.array([[1],[0],[0]])
		
		self.l = self.a * (1 - self.e**2)
		self.h = math.sqrt(self.l * self.body.mu)
		
		self.mm = math.sqrt(body.mu / self.a**3)

		
	def velocity(self, t):
		ta = self.t_to_ta(t)

		r = self.r_from_ta(ta)
		
		vr = self.h / self.l * self.e * math.sin(ta)
		vt = self.h / r

		v = np.array([[vr],[vt],[0]])

		# rotate to ellipse coordinate
		v = rotate(np.array([0,0,1]), ta) * v
		
		# rotate to global coordinate (incomplete)
		v = rotate(np.array([0,0,1]), self.aop) * v

		return v
	
	def velocity_abs(self, t):
		v = self.velocity(t)

		if self.body.orbit:
			v += self.body.orbit.velocity_abs(t)

		return v

	def arrow(self):

		p = self.position_abs(0)
		
		v = self.velocity(0) * 1000

		#print "p[0] =",p[0,0]
		
		
		w = math.sqrt(np.sum(np.square(v))) / 10
		
		arr = Arrow(p[0,0], p[1,0], v[0,0], v[1,0], w)

		return arr
		
	def ma_to_ea(self, ma):
		ea = 0

		while True:
			temp =  (ea - self.e * math.sin(ea) - ma) / (1 - self.e * math.cos(ea))
			ea -= temp
			
			if(math.fabs(temp / math.pi) < 0.001): break
			
		return ea
	def ea_to_ma(self, ea):
		ma = ea - self.e * math.sin(ea)
		return ma

	def t_to_ma(self, t):
		ma = self.ma + t * self.mm
		return ma
	def ma_to_t(self, ma):
		t = (ma - self.ma) / self.mm
		return t
	
	def t_to_ta(self, t):
		ta = self.ma_to_ta(self.t_to_ma(t))
		return ta

	def ta_to_t(self, ta):
		ma = self.ta_to_ma(ta)
		t = self.ma_to_t(ma)
		return t

	def ma_to_ta(self, ma):
		ea = self.ma_to_ea(ma)
		ta = 2 * math.atan( math.sqrt((1 + self.e)/(1 - self.e)) * math.tan(ea/2) )	
		return ta

	def ta_to_ma(self, ta):
		ea = self.ta_to_ea(ta)
		ma = self.ea_to_ma(ea)
		return ma

	def ta_to_ea(self, ta):
		ea = math.atan(math.sqrt(1 - self.e**2) * math.sin(ta) / (self.e + math.cos(ta)))
		
		if ea < 0:
			ea += math.pi

		return ea
		
	def t_to_ea(self, t):
		ma = self.t_to_ma(t)
		ea = self.ma_to_ea(t)
		return ea

	def position(self, t):
		# position vector relative to body
		
		ma = self.t_to_ma(t)
		
		ta = self.ma_to_ta(ma)

		p = rotate(np.array([0,0,1]), self.aop + ta) * self.n
		
		p *= self.r_from_ta(ta)
		
		#print "p =",p

		return p

	def ta_to_position(self, ta):
		# relative to body
		p = rotate(np.array([0,0,1]), self.aop + ta) * self.n
		p *= self.r_from_ta(ta)
		return p
			
	def ta_of_escape(self):
		if(self.apo < self.body.soi):
			return None
		
		ta = self.ta_from_r(self.body.soi)
		return ta

	def t_of_escape(self):
		ta = self.ta_of_escape()
		
		if ta is None:
			return None

		print "ta(e) = ",ta
		print "ta(0) = ",self.t_to_ta(0)
		print "ea(e) = ",self.ta_to_ea(ta)
		print "ea(0) = ",self.t_to_ea(0)
		print "ma(e) = ",self.ta_to_ma(ta)
		print "ma(0) = ",self.t_to_ma(0)

		t = self.ta_to_t(ta)
		return t


	def r_from_ta(self, ta):
		r = self.a * (1 - self.e**2) / (1 + self.e * math.cos(ta))
		return r
	def ta_from_r(self, r):
		ta = math.acos((self.a / r * (1 - self.e**2) - 1) / self.e)
		return ta
		
	def center(self):
		# center of ellipse relative to body
		
		c = -1 * self.Eu * (self.a - self.rp)
		
		return c
	def center_abs(self, t):
		c = self.center()
		
		if(self.body.orbit):
			c += self.body.orbit.position_abs(t)
		
		return c
	def position_abs(self, t):
		r = self.position(t)
		
		if(self.body.orbit):
			r += self.body.orbit.position_abs(t)
		
		return r

	def line_from_ta(self, ta):
		p0 = np.array([[0],[0],[0]])
		p1 = self.ta_to_position(ta)

		if(self.body.orbit):
			p0 += self.body.orbit.position_abs(0)
			p1 += self.body.orbit.position_abs(0)
		
		line = Line2D([p0[0,0], p1[0,0]], [p0[1,0], p1[1,0]])
		return line
		
	def ell(self):
		
		c = self.center_abs(0)

		#print "c =",c

		w = 2*self.a
		h = 2*self.b

		ell = Ellipse([c[0], c[1]], w, h, (self.aop - math.pi)/math.pi*180)
		
		return ell

	def next_orbit(self, t):
		o, t, ell, line = self.escape(t)
		
		return o, t, ell, line
		
	def escape(self, t):
		t_e = self.t_of_escape()
		
		ell = None
		line = None
		o = None

		if t_e:
			if t_e > t:
				o = orbit_1(self.body.orbit.body, o.position_abs(t_e), o.velocity_abs(t_e), t_e)
				ell = o.ell()
				line = self.line_from_ta(t_e)
		
		return o, t_e, ell, line
		

class Body:
	def __init__(self, orbit, R, soi, mu):
		self.orbit = orbit
		self.R = R
		self.soi = soi
		self.mu = mu
	def circ(self):
		p = np.array([[0],[0],[0]])

		if self.orbit:
			p += self.orbit.position_abs(0)
		
		circ = Circle([p[0], p[1]], self.R)
		
		return circ



kerbol = Body(None, 2.616E8, 1E100, 1.1723328 * 10**18)
kerbin = Body(Orbit(kerbol, 13.599840256E9, 13.599840256E9, 0, 0, 3.14), 6E5, 84.159286E6, 3.5316000E12)
mun    = Body(Orbit(kerbin, 12E6, 12E6, 0, 0, 1.7), 2E5, 2429559.1, 6.5138398E10)

o = Orbit(kerbin, 80E3, 10E6, 0, -math.pi / 2, 0)


ells = [kerbol.circ(), kerbin.circ(), kerbin.orbit.ell(), kerbin.orbit.arrow(), mun.circ(), mun.orbit.ell(), mun.orbit.arrow(), o.ell(), o.arrow()]
lines = []

t = 0

while True:
	o, t, ell, line = o.next_orbit(t)
	if o:
		ells.append(ell)
		lines.append(line)
	else:
		break
	

#ells = [kerbin.orbit.ell()]

fig = figure()
ax = fig.add_subplot(111, aspect='equal')
for e in ells:
	ax.add_artist(e)
	e.set_clip_box(ax.bbox)
	e.set_alpha(0.5)
	e.set_facecolor(rand(3))
for e in lines:
	ax.add_artist(e)


ax.set_xlim(-20e9, 20e9)
ax.set_ylim(-20e9, 20e9)

show()

a = 2
b = 0.5
r = 1
xc = 0.5

x,y = circle_ellipse(xc,0,0,0,r,a,b)

fig = figure()
ax = fig.add_subplot(111, aspect='equal')

ax.plot(x,y,'o')


ells = [Ellipse([0, 0], 2*a, 2*b), Circle([xc, 0], r)]
for e in ells:
	ax.add_artist(e)
	e.set_clip_box(ax.bbox)
	e.set_alpha(0.5)
	e.set_facecolor(rand(3))


show()



