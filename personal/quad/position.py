import numpy as np
import pylab as pl

class Position1:
	def __init__(self, c):
		self.c = c
		
		C5_11 = 0.7
		C5_22 = 0.7
		C5_33 = 0.7

		C6_11 = 3.5
		C6_22 = 3.5
		C6_33 = 3.5

		L5_11 = 0.0
		L5_22 = 0.0
		L5_33 = 0.0
		

		self.C5 = np.array([
				[C5_11,0,0],
				[0,C5_22,0],
				[0,0,C5_33]])
		self.C6 = np.array([
				[C6_11,0,0],
				[0,C6_22,0],
				[0,0,C6_33]])
		self.L5 = np.array([
				[L5_11,0,0],
				[0,L5_22,0],
				[0,0,L5_33]])
		
		self.e5 = np.zeros((c.N, 3))
		self.e6 = np.zeros((c.N, 3))
		self.chi5 = np.zeros((c.N, 3))

		self.x_ref = np.zeros((c.N, 3))
		self.x_refd = np.zeros((c.N, 3))
		self.x_refdd = np.zeros((c.N, 3))

		self.v_ref = np.zeros((c.N, 3))

		self.f_R = np.zeros((c.N, 3))
		
	def fill_xref(self, x):
		for ti in range(np.size(self.x_ref,0)):
			self.x_ref[ti] = x
	def get_f6(self, e5, e6):
		return -np.dot(self.C6,e6) - e5
	def step(self, ti):
		dt = self.c.t[ti] - self.c.t[ti-1]
		
		# reference
		self.x_refd[ti] = (self.x_ref[ti] - self.x_ref[ti-1]) / dt
		
		if ti > 1:
			self.x_refdd[ti] = (self.x_refd[ti] - self.x_refd[ti-1]) / dt
		
		# tracking error
		self.e5[ti] = self.x_ref[ti] - self.c.x[ti]
		self.chi5[ti] = self.chi5[ti-1] + self.e5[ti] * dt
		
		# step v_ref before stepping e6
		self.v_ref[ti] = np.dot(self.C5, self.e5[ti]) + self.x_refd[ti] + np.dot(self.L5, self.chi5[ti])
		
		# step velocity error
		self.e6[ti] = self.v_ref[ti] - self.c.v[ti]
		 
	def get_force_rotor(self, ti):
		e5 = self.e5[ti]
		e6 = self.e6[ti]
		chi5 = self.chi5[ti]
		
		f6 = self.get_f6(e5,e6)

		C5 = self.C5
		L5 = self.L5
		
		m = self.c.m
		g = self.c.gravity		

		f_D = self.c.get_force_drag(ti)

		x_refdd = self.x_refdd[ti]
		
		temp1 = np.dot(C5, e6 - np.dot(C5, e5) - np.dot(L5, chi5))
		
		temp2 = np.dot(L5, e5)
		
		f_R = m * (-f6 + temp1 + x_refdd + temp2 - g) - f_D
		
		self.f_R[ti] = f_R
		
			
		ver = True
		ver = False
		if ver:
			print 'f6   ' ,f6
			print 'temp1' ,temp1
			print 'xrefdd',xrefdd
			print 'temp2 ',temp2
			print 'g     ',g
			print 'f_D   ',f_D
			print 'f_R   ',f_R

		return f_R
	def plot(self):
		t = self.c.t
		
		# f
		fig = pl.figure()
		
		ax = fig.add_subplot(111)
		ax.set_ylabel('f_R')
		
		ax.plot(t, self.f_R)

		# x
		fig = pl.figure()
		
		x = self.c.x[:,0]
		y = self.c.x[:,1]
		z = self.c.x[:,2]
		xr = self.x_ref[:,0]
		yr = self.x_ref[:,1]
		zr = self.x_ref[:,2]
		
		ax = fig.add_subplot(111)
		ax.set_xlabel('t')
		ax.set_ylabel('x')
		
		ax.plot(t,x,'b-')
		ax.plot(t,y,'g-')
		ax.plot(t,z,'r-')
		ax.plot(t,xr,'b--')
		ax.plot(t,yr,'g--')
		ax.plot(t,zr,'r--')
		
		ax.legend(['x','y','z','xr','yr','zr'])
		
		# v
		fig = pl.figure()
		
		x = self.c.v[:,0]
		y = self.c.v[:,1]
		z = self.c.v[:,2]
		xr = self.v_ref[:,0]
		yr = self.v_ref[:,1]
		zr = self.v_ref[:,2]
		
		ax = fig.add_subplot(111)
		ax.set_xlabel('t')
		ax.set_ylabel('v')
		
		ax.plot(t,x,'b-')
		ax.plot(t,y,'g-')
		ax.plot(t,z,'r-')
		ax.plot(t,xr,'b--')
		ax.plot(t,yr,'g--')
		ax.plot(t,zr,'r--')
		
		ax.legend(['x','y','z','xr','yr','zr'])
		
		# e	
		fig = pl.figure()
		
		ax = fig.add_subplot(221)
		ax.set_ylabel('e_5')
		ax.plot(t, self.e5)
	
		ax = fig.add_subplot(222)
		ax.set_ylabel('e_6')
		ax.plot(t, self.e6)
		
	
	
	
