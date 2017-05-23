import numpy as np
import logging

from unit_vec import *

class equation_prob:
	def __init__(self, prob, name, k, alpha, alpha_source):
		self.prob = prob
		self.name = name
		self.k = k
		self.alpha = alpha
		self.alpha_source = alpha_source

class Equ:
	# diffusion equation variable set

	def __init__(self, name, face, equ_prob):
		self.name = name
		self.face = face
		
		self.equ_prob = equ_prob

		#self.v_0 = v_0
		
		self.n_extended = self.face.n + np.array([2, 2])
		
		self.v = np.ones(self.n_extended) * self.face.patch.group.v_0[self.name]
		
		print "equation"
		print "name",self.name
		print "v_0",self.face.patch.group.v_0[self.name]

		self.s = np.ones(face.n)
		
		self.flag = {"only_parallel_faces":False}
		
	def grad(self):
		return np.gradient(self.v[:-2,:-2], self.face.d[0,0,0], self.face.d[0,0,1])
	def grad_mag(self):
		return np.sqrt(np.sum(np.square(self.grad()),0))
	
	def min(self):
		return np.min(self.v[:-2,:-2])
	def max(self):
		v = np.max(self.v[:-2,:-2])
		#print "v"
		#print self.v
		#print "max"
		#print v
		return v
	def grad_min(self):
		return np.min(self.grad_mag()[:-2,:-2])
	def grad_max(self):
		return np.max(self.grad_mag()[:-2,:-2])
	
	def mean(self):
		return np.mean(self.v[:-2,:-2])
	def point(self, pt):
		
		# global coor cooresponding to local coors
		Xg = self.face.loc_to_glo(1)
		Yg = self.face.loc_to_glo(2)
		Zg = self.face.loc_to_glo(3)
		
		xg,sxg = v2is(Xg)
		yg,syg = v2is(Yg)
		zg,szg = v2is(Zg)

		# is point in face extents
	
		def debug():
			print 'equ point'
			print xg,yg,zg
			print sxg,syg,szg
			print pt
			print self.face.ext

		if pt[xg] < self.face.ext[0,0]:
			logging.debug("x {0} < {1}".format(pt[xg],self.face.ext[0,0]))
			return None
		if pt[xg] > self.face.ext[0,1]:
			logging.debug("x {0} > {1}".format(pt[xg],self.face.ext[0,1]))
			return None
		if pt[yg] < self.face.ext[1,0]:
			logging.debug("y {0} > {1}".format(pt[yg],self.face.ext[1,0]))
			return None
		if pt[yg] > self.face.ext[1,1]:
			logging.debug("y {0} > {1}".format(pt[yg],self.face.ext[1,1]))
			return None
		
		if pt[zg] != self.face.pos_z:
			logging.debug("z")
			return None

		i = (pt[xg] - self.face.ext[0,0]) / self.face.d[0,0,0]
		j = (pt[yg] - self.face.ext[1,0]) / self.face.d[0,0,1]
		
		i = round(i)
		j = round(j)

		#print 'equ point i,j',i,j

		return self.v[i,j]


