import math
import inspect
import numpy as np
import multiprocessing
from matplotlib import cm
import pylab as pl
import logging

from unit_vec import *

import equation

class Conn:
	# information concerning connection between face and conn
	# from perspective of face
	def __init__(self, face, conns):
		self.face = face
		self.conns = conns
		
		self.MP = False
		
		# needed to store boundary values for multiple equs
		self.equs = {}

	def refresh(self):
		self.OL = self.face.nbr_to_loc(self.twin.face)
		
		self.ol, self.sol = v2is(self.OL)
		
		self.PL = abs(cross(3, self.OL))
		self.pl,_ = v2is(self.PL)

		self.PG = self.face.loc_to_glo(self.PL)
		
		self.li, self.lj, self.d = self.face.index_lambda(self.twin.face)
		
		#self.printinfo()

	def printinfo(self):
		print "face",self.face.Z
		print "nbr ",self.twin.face.Z
		print "li lj"
		print inspect.getsource(self.li)
		print inspect.getsource(self.lj)
	def send(self, name, v):
		if self.MP:
			self.conns[name].send(v)
		else:
			self.equs[name] = v
	
	def recv(self, name):
		n = self.face.n[self.pl]

		if self.MP:
			v = self.conns[name].recv()
		else:
			try:
				v = self.twin.equs[name]
			except:
				#print "warning: array not available"
				v = np.zeros(n)
		
		return v

	
	


class Face(LocalCoor):
	def __init__(self, patch, normal, ext, pos_z, n):
		LocalCoor.__init__(self, normal)
	
		self.patch = patch

		self.ext = np.array(ext)
		
		self.pos_z = pos_z
		
		self.n = np.array(n)
		
		# the extra 2 rows/cols are for storing neighbor values
		n_extended = self.n + np.array([2, 2])
		
		
		self.d = np.zeros((n_extended[0], n_extended[1], 2))
		for i in range(n_extended[0]):
			for j in range(n_extended[1]):
				self.d[i,j,:] = (self.ext[:,1] - self.ext[:,0]) / np.float32(self.n)
		
		
		if np.any(self.d < 0):
			print self.d
			raise ValueError('bad')
		
		self.conns = np.empty((2,2), dtype=object)
		
		# source
		self.l = np.array([
			(self.ext[0,1] - self.ext[0,0]) / 2.0,
			(self.ext[1,1] - self.ext[1,0]) / 2.0])
		
		
		a = self.l[0] / 2.
		b = self.l[1] / 2.
		
		x = np.linspace(self.d[0,0,0] / 2. - a, a - self.d[0,0,0] / 2., self.n[0])
		y = np.linspace(self.d[0,0,1] / 2. - b, b - self.d[0,0,1] / 2., self.n[1])
		Y,X = np.meshgrid(y,x)
		
	
		self.Tmean = []

		self.equs = {}

	def create_equ(self, name, equ_prob):
		self.equs[name] = equation.Equ(name, self, equ_prob)
	
	def get_loc_pos_par_index(self, nbr):
		OL = self.nbr_to_loc(nbr)
		
		PL = abs(cross(3, OL))
		
		PG = self.loc_to_glo(PL)
		return PG
		
	def x(self, i):
		return (i + 0.5) * self.d[0]
		
	def y(self, j):
		return (j + 0.5) * self.d[1]
	
	def area(self):
		return (self.ext[0,1] - self.ext[0,0]) * (self.ext[1,1] - self.ext[1,0])

	def nbr_to_loc(self, nbr):
		if not isinstance(nbr, Face):
			raise ValueError('nbr is not Face')
		if not nbr:
			raise ValueError('nbr is None')
		
		for i in range(2):
			for j in range(2):
				conn = self.conns[i,j]
				if conn:
					if nbr == conn.twin.face:
						return is2v(i,2*j-1)
		
		print [conn.nbr if conn else conn for conn in self.conns.flatten()]
		print nbr
		raise ValueError('nbr not found')

	def loc_to_conn(self, V):
		v,sv = v2is(V)
		return self.conns[v, (sv+1)/2]

	def index_lambda(self, nbr):
		# returns lambda:
		# function of positive parallel index of neighbor
		# returns the index of my cell
				
		if not isinstance(nbr, Face):
			raise ValueError('nbr is not a Face')
		
		# PG global index of neighbor's positive parallel local index
		PG = nbr.get_loc_pos_par_index(self)
		
		PL = self.glo_to_loc(PG)
		OL = self.nbr_to_loc(nbr)
		
		pl,spl = v2is(PL)
		ol,sol = v2is(OL)
		
		d = self.d[ol]
		
		l = [None,None]
		l[pl] = lambda p, pl=pl, spl=spl: p if (spl > 0) else self.n[pl] - p - 1
		l[ol] = lambda p, ol=ol, sol=sol: 0 if (sol < 0) else (self.n[ol] - 1)
		
		#print inspect.getsource(i)
		#print inspect.getsource(j)
		#print l

		return l[0],l[1],d
	
	def send_array(self, equ, conn):
		
		v = np.ones(self.n[conn.pl])
		
		for a in range(self.n[conn.pl]):
			v[a] = equ.v[conn.li(a), conn.lj(a)]
		
		conn.send(equ.name, v)
		
	def recv_array(self, equ, conn):
		v = conn.recv(equ.name)
		
		ind = [0,0]
		ind[conn.ol] = -1 if conn.sol < 0 else self.n[conn.ol]
		
		for a in range(self.n[conn.pl]):
			ind[conn.pl] = a
			
			equ.v[ind[0],ind[1]] = v[a]
		
	def term(self, equ, ind, v, sv, To):
		# get the value and coefficienct for the cell adjacent to ind in the direction V

		d = self.d[ind[0],ind[1],v]

		# interior cells and boundary cells with Face neighbors
		indnbr = list(ind)
		indnbr[v] += sv
		
		y = equ.v[indnbr[0],indnbr[1]]
		
		#print ind,indnbr
		#print "T",T,"To",To
		
		d_nbr = self.d[indnbr[0],indnbr[1],v]
		
		a = 2.0 / (d + d_nbr)
		
		return a,y

	def step_pre_cell(self, equ, ind, V):
		# set the v-array value for the boundary value at ind+V
		
		v,sv = v2is(V)
		
		conn = self.loc_to_conn(V)
		if conn:
			if equ.flag["only_parallel_faces"] == True:
				if conn.twin.face.Z == self.Z:
					self.recv_array(equ, conn)
				else:
					self.step_pre_cell_open_bou(equ, ind, V)
			else:
				self.recv_array(equ, conn)
		else:
			self.step_pre_cell_open_bou(equ, ind, V)

	def step_pre_cell_open_bou(self, equ, ind, V):
		logging.debug('step_pre_cell_open_bou')
		
		v,sv = v2is(V)
		indn = list(ind)
		indn[v] += sv
		
		p = 0 if v==1 else 1
		
		logging.debug("V    {0}".format(V))
		logging.debug("ind  {0}".format(ind))
		logging.debug("indn {0}".format(indn))
		
		# get stored boundary value
		v_bou = self.v_bou[equ.name][v][(sv+1)/2]

		if isinstance(v_bou,float):
			pass
		else:
			v_bou = v_bou[ind[p]]
		
		if v_bou == 0.0: # insulated
			equ.v[tuple(indn)] = equ.v[tuple(ind)]
		else: # constant temperature
			equ.v[tuple(indn)] = 2.0 * v_bou - equ.v[tuple(ind)]
		


	def step_pre(self, equ):
		# for boundaries, load boundary temperature cells with proper value
		# west/east
		for j in range(self.n[1]):
			self.step_pre_cell(equ, [          0, j], -1)
			self.step_pre_cell(equ, [self.n[0]-1, j],  1)
		
		# north/south
		for i in range(self.n[0]):
			self.step_pre_cell(equ, [i,           0], -2)
			self.step_pre_cell(equ, [i, self.n[1]-1],  2)
		
	def step(self, equ_name):
		equ = self.equs[equ_name]

		if not isinstance(equ, equation.Equ):
			raise ValueError('not Equ')

		# solve diffusion equation for equ
		
		R = 0.0
		
		ver1 = False
		#ver1 = True
		
		ver2 = False
		
		
		# solve equation

		self.step_pre(equ)

		g = self.patch.group
		S = g.S[equ.name]

		#print "face S",S

		def debug_s():
			print "face s",s
			print "s",equ.s[i,j]
			print "A",A
			print "k",equ.equ_prob.k

		for i in range(self.n[0]):
			for j in range(self.n[1]):
				A = self.d[i,j,0] * self.d[i,j,1]
				
				yo = equ.v[i,j]

				aW, yW = self.term(equ, [i,j],0,-1, yo)
				aE, yE = self.term(equ, [i,j],0, 1, yo)
				aS, yS = self.term(equ, [i,j],1,-1, yo)
				aN, yN = self.term(equ, [i,j],1, 1, yo)
				
				#ver = True
				#print "source =",self.s(To)
				
				# source term
				s = equ.s[i,j] * S * A / equ.equ_prob.k

				#if s < 0:
				#debug_s()
				
				
				num = aW*yW + aE*yE + aS*yS + aN*yN + s
				ys = num / (aW + aE + aS + aN)
				
				dy = equ.equ_prob.alpha * (ys - yo)

				def debug():
					print "aW aE aS aN"
					print aW, aE, aS, aN
					print "yW yE yS yN yo ys dy"
					print yW, yE, yS, yN, yo, ys, dy
				
				#debug()
				
				if aW < 0 or aE < 0 or aS < 0 or aN < 0:
					debug()
					raise ValueError('bad')

				if ver1: debug()

				if math.isnan(yo):
					raise ValueError('nan')
				if math.isnan(ys) or math.isinf(ys):
					debug()
					raise ValueError('bad')
				if math.isnan(dy):
					raise ValueError('nan')
			 
				equ.v[i,j] += dy
				
				if dy == 0.0:
					pass
				else:
					R = max(math.fabs(dy/yo), R)
				
				if math.isnan(R):
					print 'dy',dy,'yo',yo
					raise ValueError('nan')
		return R

	def send(self, equ_name):
		# send/recv neighbor values
		equ = self.equs[equ_name]
		
		for con in self.conns.flatten():
			if con:
				self.send_array(equ, con)
	
	def recv(self, equ_name):
		equ = self.equs[equ_name]

		for con in self.conns.flatten():
			if con:
				self.recv_array(equ, con)
		
	def plot3(self, ax, T_max):
		x = [0]*3

		Xdir = abs(self.loc_to_glo(1)) - 1
		Ydir = abs(self.loc_to_glo(2)) - 1
		Zdir = abs(self.loc_to_glo(3)) - 1
		
		x[Xdir] = np.linspace(self.ext[0,0],self.ext[0,1],self.n[0])
		x[Ydir] = np.linspace(self.ext[1,0],self.ext[1,1],self.n[1])

		#print "glo", Xdir, Ydir, Zdir
		#print "x", x[Xdir]
		#print "y", x[Ydir]
		
		# x and y
		#x[Ydir],x[Xdir] = np.meshgrid(x[Ydir], x[Xdir])
		x[Xdir],x[Ydir] = np.meshgrid(x[Xdir], x[Ydir])

		# z
		#x[Zdir] = np.ones((self.n[0],self.n[1])) * self.z
		x[Zdir] = np.ones((self.n[1],self.n[0])) * self.pos_z

		# T
		T = self.T[:-2,:-2]

		if self.zs > 0:
			T = np.transpose(T)
		else:
			T = np.rot90(T,1)
			T = np.fliplr(T)
		
		

		FC = cm.jet(T/T_max)

		#print np.shape(x[0])
		#print np.shape(x[1])
		#print np.shape(x[2])
		#print np.shape(FC)

		ax.plot_surface(x[0], x[1], x[2], rstride=1, cstride=1, facecolors=FC, shade=False)
		
	def plot(self, equ_name, ax1, ax2, V = None, Vg = None):
		equ = self.equs[equ_name]
		
		con1 = self.plot_temp_sub(equ, ax1, V)
		
		con2 = self.plot_grad_sub(equ, ax2, Vg)

		return con1, con2
	def grid(self, equ_name):
		x = np.linspace(self.ext[0,0], self.ext[0,1], self.n[0])
		y = np.linspace(self.ext[1,0], self.ext[1,1], self.n[1])
		
		X,Y = np.meshgrid(x,y)
		
		Z = np.ones(np.shape(X)) * self.pos_z

		equ = self.equs[equ_name]
		
		W = equ.v[:-2,:-2]
		
		if self.zs > 0:
			W = np.transpose(W)
		else:
			W = np.rot90(W,1)
			W = np.fliplr(W)

		return X,Y,Z,W

	def plot_temp_sub(self, equ, ax, V = None):
		X,Y,_,W = self.grid(equ.name)
		
		ver = False
		if ver:
			print np.shape(X)
			print np.shape(Y)
			print np.shape(T)
		
		if not V is None:
			con = ax.contourf(X, Y, W, V)
		else:
			con = ax.contourf(X, Y, W)
		
		return con

	def plot_grad_sub(self, equ, ax, V = None):
		x = np.linspace(self.ext[0,0], self.ext[0,1], self.n[0])
		y = np.linspace(self.ext[1,0], self.ext[1,1], self.n[1])

		X,Y = np.meshgrid(x,y)
		
		# values	
		Z = equ.grad_mag()
			
		if self.zs > 0:
			Z = np.transpose(Z)
		else:
			Z = np.rot90(Z,1)
			Z = np.fliplr(Z)



		ver = False
		if ver:
			print "plot_grad_sub"
			print np.shape(X)
			print np.shape(Y)
			print np.shape(Z)

		if not V is None:
			con = ax.contourf(X, Y, Z, V)
		else:
			con = ax.contourf(X, Y, Z)

		return con

	def plot_grad(self, V = None):
		x = np.linspace(self.ext[0,0], self.ext[0,1], self.n[0])
		y = np.linspace(self.ext[1,0], self.ext[1,1], self.n[1])
		
		X,Y = np.meshgrid(x, y)
		
		T = np.transpose(self.T)

		Z = np.gradient(T, self.d[0], self.d[1])
		Z = np.sqrt(np.sum(np.square(Z),0))
		
		
		#print np.shape(self.T)
		#print np.shape(Z)
		
		fig = figure()
		ax = fig.add_subplot(111)

		if not V is None:
			con = ax.contourf(X, Y, Z, V)
		else:
			con = ax.contourf(X, Y, Z)
		
		pl.colorbar(con)
		pl.axis('equal')

		return con


def connect(f1, a1, b1, f2, a2, b2, multi = False):
	if multi:
		c1, c2 = multiprocessing.Pipe()
	else:
		c1, c2 = None, None
	
	conn1 = Conn(f1, c1)
	conn2 = Conn(f2, c2)
	
	conn1.twin = conn2
	conn2.twin = conn1
	
	#f1.nbrs[a1,b1] = f2
	#f2.nbrs[a2,b2] = f1
	
	f1.conns[a1,b1] = conn1
	f2.conns[a2,b2] = conn2
	
	conn1.refresh()
	conn2.refresh()

