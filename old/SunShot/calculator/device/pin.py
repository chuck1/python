import os
import sys
import math
from lxml import etree

#sys.path.append('~/Programming/Python/Modules')
sys.path.append('/nfs/stak/students/r/rymalc/Programming/Python/Modules')

import vector
from Sci import Fluids


class pin:
	def __init__(self):
		self.names_float = ['r','PL','D','T0','T1','qpp','N','z0','z1'];
		self.names_string = ['fluid_str'];
		
	def load( self, filename ):
		tree = etree.parse( filename )
		
		root = tree.getroot()
		
		for child in list(root):
			self.load_var( child )
		
	def load_var( self, node ):
		name = node.tag
		
		if name in self.names_float:
			value = float( node.text )
			setattr( self, name, value )
			print "set %r to %f" % ( name, value )
		elif name in self.names_string:
			value = node.text.strip()
			
			setattr( self, name, value )
			
			print "set %r to %r" % ( name, value )

		else:
			print "%r not valid" % name
		
		
		
	def run( self ):
		self.fluid = Fluids.Fluid( self.fluid_str + '.xml' )
		
		self.dh = self.fluid.enthalpy_change( self.T0, self.T1 )
		
		print 'dh=%f' % self.dh
		
		self.PD = self.PL * self.r

		self.PT = math.sqrt( pow( self.PD, 2 ) - pow( self.PL / 2.0, 2 ) )
		
		self.SL = self.PL * self.D
		self.ST = self.PT * self.D
		
		
		
		self.L = self.SL * ( self.N + 0.5 ) + self.z0 + self.z1
		self.W = self.ST
		
		
		self.m = self.qpp * self.L * self.W / self.dh

		print "m={0}".format( self.m )
