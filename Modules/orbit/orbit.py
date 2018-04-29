#!/usr/bin/env python

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import itertools
import numpy as np
import math
import sys

sys.path.append("/nfs/stak/students/r/rymalc/Documents/python")

import vector
import system

z_axis = np.array([0,0,1])


G = 6.674e-11

def sphere( ax, r ):
	u = np.linspace(0, 2 * np.pi, 100)
	v = np.linspace(0, np.pi, 100)
	
	x = r * np.outer(np.cos(u), np.sin(v))
	y = r * np.outer(np.sin(u), np.sin(v))
	z = r * np.outer(np.ones(np.size(u)), np.cos(v))
	ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='g')


class orbit_elip:
	def v( self, r ):
		return math.sqrt( self.parent.mu * ( ( 2.0 / r ) - ( 1 / self.a ) ) )
	def __init__( self, parent, alt_a, alt_p ):
		self.parent = parent
		
		self.alt_p = alt_p
		self.alt_a = alt_a
		self.ra = alt_a + parent.radius
		self.rp = alt_p + parent.radius
		
		self.a = ( self.ra + self.rp ) / 2.0
		self.c = ( self.ra - self.rp ) / 2.0
		self.e = self.c / self.a
		
		self.va = self.v( self.ra )
		self.vp = self.v( self.rp )
		
		self.P = 2.0 * math.pi * math.sqrt( pow(self.a,3) / self.parent.mu )

	def theta( self, t ):
		return 2.0 * math.pi * t / self.P
class orbit_circ:
	def __init__( self, parent, alt ):
		self.parent = parent
		self.alt = alt
		
		self.r = self.alt + parent.radius
		
		self.v = math.sqrt( parent.mu / self.r )
		
		self.P = 2.0 * math.pi * math.sqrt( pow(self.r,3) / self.parent.mu )

	def theta( self, t ):
		return 2.0 * math.pi * t / self.P



def axis_equal_3d( ax ):
	w_lims = ax.get_w_lims()
	x_min = w_lims[0]
	x_max = w_lims[1]
	y_min = w_lims[2]
	y_max = w_lims[3]
	z_min = w_lims[4]
	z_max = w_lims[5]
	
	x_d = x_max - x_min
	y_d = y_max - y_min
	z_d = z_max - z_min
	
	w_min = min( [w_lims[0], w_lims[2], w_lims[4]] )
	w_max = max( [w_lims[1], w_lims[3], w_lims[5]] )
	w_d = w_max - w_min
	
	x_min -= ( w_d - x_d ) / 2.0
	x_max += ( w_d - x_d ) / 2.0
	y_min -= ( w_d - y_d ) / 2.0
	y_max += ( w_d - y_d ) / 2.0
	z_min -= ( w_d - z_d ) / 2.0
	z_max += ( w_d - z_d ) / 2.0
	
	ax.set_xlim3d( x_min, x_max )
	ax.set_ylim3d( y_min, y_max )
	ax.set_zlim3d( z_min, z_max )




