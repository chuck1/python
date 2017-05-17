import os
import math
import re
import sys
from lxml import etree
import numpy as np
import logging

modules_dir = os.environ["HOME"] + '/Programming/Python/Modules/'
media_dir = modules_dir + 'Sci/media/'

FILE = os.path.abspath(__file__)
h,t = os.path.split(FILE)
media_dir = os.path.join(h,'media')
print(media_dir)

def get_child_by_attr(root,attr,value):
	for child in list(root):
		if child.get(attr) == value:
			return child
	return None

def process_element(root):
	#print root.tag
	for child in list(root):
		process_element(child)

class Poly:
	def __init__( self, node ):
		text = node.text
		text = re.sub('[\s\n]*','',text)
		split = re.split(",", node.text)
		
		self.a = np.array([])
		
		#print 'poly tag =', node.tag, "attr =",node.attrib
		
		#print 'poly text=%r' % node.text
		#print 'split {0}'.format( split )
		
		# process coefficients
		for s in split:
			v = float(s)
			self.a = np.append(self.a, v)
	
		#print "a =",self.a

	def eval( self, X ):
		#print "X",X
		if isinstance(X, float):
			Y = np.array( [X]*len(self.a) )
			
			z = np.sum( self.a * np.power( Y, range(len(self.a)) ) )

			return z
		elif isinstance(X, np.ndarray):
			Z = np.array([])
			for x in X:
				Y = np.array([x] * len(self.a))
				#print "Y",Y
				
				t1 = np.power(Y, range(len(self.a)))
				#print "a ",self.a,np.shape(self.a)
				#print "t1",t1,np.shape(t1)
				#print "--",self.a[0] * t1[0]
				#if len(self.a) > 1:
				#print "--",self.a[1] * t1[1]

				#print np.multiply(self.a, t1)

				z = np.sum(self.a * np.power(Y, range(len(self.a))))

				Z = np.append(Z,z)
			return Z
		else:
			logging.info(type(X))
			raise TypeError()
	def integrate( self, X ):
		Y = self.eval( X )
		Z = integ( X, Y )
		return Z

		
class Property:
	def __init__( self, node ):
		self.poly = []
		
		#print 'prop tag=',node.tag
		
		for child in list(node):
			self.poly.append( Poly( child ) )
		
		
		
class Fluid:
	def __init__( self, filename ):
		self.dict = {}
		
		filename = filename + ".xml"
		
		
		tree = etree.parse( os.path.join(media_dir, filename) )
		root = tree.getroot()
	

		#print "parsing '{0}'".format(media_dir + filename)
		#print 'root tag=%r' % root.tag

	
		# process children
		for child in list(root):
			name = child.get( 'name' )
			#print 'name=%r' % name
			
			if name:
				self.dict[name] = Property( child )
		
		
	def get( self, prop_name, T ):
		if prop_name in self.dict:
			prop = self.dict[prop_name]
		else:
			logging.info("properties:")
			logging.info(self.dict)
			raise Exception("property not found")
		
		
		poly = prop.poly[0]
		
		return poly.eval( T )

	def list(self):
		"""list properties"""
		for k,v in self.dict.items():
			logging.info(k)
		
	def enthalpy_change( self, T0, T1 ):
		T0 = np.array(T0)
		T1 = np.array(T1)

		X = np.linspace(T0,T1,100)
		#X = frange( T0, T1, 1 )
		
		return self.dict['cp'].poly[0].integrate( X );
	def Pr(self, T):
		cp = self.get('cp',T)
		mu = self.get('dynamic_viscosity',T)
		k = self.get('thermal_conductivity',T)
		
		logging.info("{} {} {}".format(cp,mu,k))

		Pr = cp * mu / k
		return Pr

def integ(X,Y):
	l = len(X)
	return np.sum( ( Y[:l-1] + Y[1:] ) * ( X[1:] - X[:l-1] ) / 2 )



def np_array(X):
	if not isinstance(X,np.ndarray):
		if isinstance(X,list):
			X = np.array(X)
		else:
			X = np.array([X])
	return X


def frange(start,stop,step):
	r = start
	x = np.array(())
	while r <= stop:
		x = np.append(x,r)
		r += step
	return x


if __name__ == "__main__":
	import Sci.Fluids
	help(Sci.Fluids)
	
	f = Sci.Fluids.Fluid('co2')
	f.list()


