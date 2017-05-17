#!/usr/bin/env python

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import itertools
import numpy as np
import math
import sys

sys.path.append("/nfs/stak/students/r/rymalc/Documents/python")

import vector

def progress( value0, value1 ):
	bar_length0 = 40
	bar_length1 = 40
	
	block0 = int( round( bar_length0 * value0 ) )
	block1 = int( round( bar_length1 * value1 ) )


	text = "\rprogress: [{0}][{1}]".format( "0"*block0 + "1"*(bar_length0 - block0), "0"*block1 + "1"*(bar_length1 - block1) )
	sys.stdout.write(text)
	sys.stdout.flush()


z_axis = np.array([0,0,1])


G = 6.674e-11

def fd1( y0, yp0, yp1, dx ):
	y1 = y0 + 0.5 * ( yp0 + yp1 ) * dx
	return y1

def fd0( y0, yp0, dx ):
	y1 = y0 + yp0 * dx
	return y1



class sat:
	def init_abs( self, radius, mass, init_X ):
		self.radius = radius
		self.mass = mass
		self.mu = G * self.mass
		self.init_X = init_X
		self.init_V = np.zeros(3)
	def init_rel( self, parent, radius, alt, speed, init_lati, init_long, mass ):
		self.parent = parent
		self.alt = alt
		self.speed = speed
		self.init_lati = init_lati
		self.init_long = init_long
		self.mass = mass
		self.mu = G * self.mass

		init_x = math.cos(init_lati) * math.cos(init_long)
		init_y = math.cos(init_lati) * math.sin(init_long)
		init_z = math.sin(init_lati)
		
		
		init_uX = vector.norm( np.array([init_x,init_y,init_z]) )
		init_uV = vector.norm( np.cross( z_axis, init_uX ) )

		self.init_X = init_uX * ( alt + parent.radius )
		self.init_V = init_uV * speed

	def init_run( self, nt ):
		self.x = np.zeros((nt,3))
		self.v = np.zeros((nt,3))
		self.f = np.zeros((nt,3))
		self.a = np.zeros((nt,3))
		self.V = np.zeros(nt)
		self.A = np.zeros(nt)
		self.c0 = np.zeros(nt)
				
		self.x[0,:] = np.array( self.init_X )
		self.v[0,:] = np.array( self.init_V )

		#self.stats(0)

	def stats( self, i ):
		self.V[i] = vector.magn( self.v[i,:] )
		self.A[i] = vector.magn( self.a[i,:] )
		self.c0[i] = self.V[i]/self.A[i]

		#print "sat V  = ",self.V[i]
		#print "sat A  = ",self.A[i]
		#print "sat c0 = ",self.c0[i]
	def accel( self, i ):
		# acceleration
		self.a[i,:] = self.f[i,:] / self.mass

				
	def step( self, dt, i ):
		v_old = np.array( self.v[i,:] )

		# velocity
		self.v[i,:] = fd1( self.v[i-1,:], self.a[i-1,:], self.a[i,:], dt )
		
		#print self.a[i-1,:]	
		#print self.a[i,:]
		#print v_old
		#print self.v[i,:]
		
		#self.x[i,:] = fd0( self.x[i-1,:], self.v[i-1,:], dt )
		self.x[i,:] = fd1( self.x[i-1,:], self.v[i-1,:], self.v[i,:], dt )
		
		V_delta = vector.magn( self.v[i,:] - v_old )
		V_old = vector.magn( v_old )
		
		#print "V_delta",V_delta,"V_old",V_old
		
		if V_old == 0:
			if V_delta == 0:
				return 0
			else:
				return 1
		else:
			return V_delta / V_old
		
		
	def plot_traj( self, ax, i ):
		ax.plot( self.x[0:i,0], self.x[0:i,1], self.x[0:i,2] )
	def plot_sphere( self, ax ):
		sphere( ax, self.radius )
	def plot_2dtraj( self, ax, i ):
		ax.plot( self.x[0:i,0], self.x[0:i,1] )

class system:
	def __init__( self, sats ):
		self.sats = sats
		self.nb_sats = len(sats)
		self.pairs = list( itertools.combinations( range(self.nb_sats), 2 ) )
		
	def run( self, nt, tf ):
		self.tf = tf
		self.nt = nt
		self.dt = np.zeros(nt)
		self.t = np.zeros(nt)
		self.c0 = np.zeros(nt)
		
		for a in range(self.nb_sats):
			self.sats[a].init_run( nt )
		
		str_break = "maximum number of iterations reached"

		
		# loop
		for i in range(nt):
			try:			
				if i==0:
					self.step0()
				else:
					self.step(i)
			except:
				str_break = "error occured"
				break
			
			#print "time = ",self.t[i],"dt = ",self.dt[i]
	
			progress( self.t[i] / tf, float(i) / float(nt) )
			
			if self.t[i] > self.tf:
				str_break = "final time reached"
				break

		print
		print str_break
		
		return i
		
	def init_next_x( self, i ):
		if i < (self.nt-1):
			for s in self.sats:
				s.x[i+1] = np.array( s.x[i] )
				s.v[i+1] = np.array( s.v[i] )

	def accel( self, i ):
		# reset force
		for a in range(self.nb_sats):
			self.sats[a].f[i,:] = 0
		
		# calculate force
		for a in range(len( self.pairs )):
			b = self.pairs[a][0]
			c = self.pairs[a][1]
	
			r = self.sats[b].x[i,:] - self.sats[c].x[i,:]
			
			d = vector.magn( r )
			
			if d == 0:
				raise Exception("error: d=0")
			else:
				f = G * self.sats[b].mass * self.sats[c].mass / d / d * ( r / d )
			
			self.sats[b].f[i,:] -= f
			self.sats[c].f[i,:] += f
	
		
		for s in self.sats:
			s.accel(i)
		
	def stats( self, i ):
		c0 = np.zeros(self.nb_sats)
		for a in range(self.nb_sats):
			self.sats[a].stats(i)
			c0[a] = self.sats[a].c0[i]

		self.c0[i] = np.min(c0)
		
		#print "c0 = ",self.c0[i]
		
	def step0( self ):
		self.accel(0)
		self.init_next_x(0)
		self.stats(0)
		self.time_step(0)

	def time_step( self, i ):
		dt_min = 1.0
		dt_max = 400.0
		dt = self.c0[i] / 400.0
		
		self.dt[i] = min( max( dt, dt_min ), dt_max )
		
		
	def step( self, i ):
		self.init_next_x(i)
		
		self.t[i] = self.t[i-1] + self.dt[i-1]
		
		max_it = 100
		for it in range(max_it+1):
			self.accel(i)
			
			e = 0
			for a in range(self.nb_sats):
				e += self.sats[a].step( self.dt[i-1], i )
			
			#print "e",e
			
			if e < 0.000001:
				break
		
		if it == max_it:
			raise Exception("maximum inner iterations reached")
		
		self.stats(i)
		self.time_step(i)
