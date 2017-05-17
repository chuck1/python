import math
import numpy as np
import matplotlib.pyplot as plt

def numpy_invertible(A,Z):
	try:
		B = np.linalg.solve(A,Z)
		return (B,True)
	except np.linalg.linalg.LinAlgError:
		return (None,False)


def index(a,m):
	if np.ndim(m) != 1:
		raise Exception("m must be 1D array")
	n = np.size(m,0)
	v = np.zeros( (n,1) )
	b = a
	v[0] = b % m[0]
	for c in range(1,n):
		b = ( b - v[c-1] ) / m[c-1]
		v[c] = b % m[c]
	return v


def bicub_matrix(x,m):
	print "bicub_matrix"
	#print m
	n = np.size(m,0)
	p = np.prod(m)
	
	A = np.zeros( (p,p) )
	
	for a in range(0,p): # row
		for b in range(0,p): # col
			# i = array of power for each of the n variables
			i = index(b,m)
			A[a][b] = 1
			for c in range(0,n):
				A[a][b] *= pow( x[a][c], i[c] )
	return A
	

class spline:
	m = np.array([])
	n = 0
	p = 0
	B = np.matrix([])
	def __init__(self,m,x,z):
		
		if np.ndim(m) != 1:
			raise Exception("m must be 1D array")

		n = np.size(m,0)
		p = np.prod(m)

		if n == 1:
			print np.shape(x)
			print p
			x = np.reshape( x, (p,1) )
		
		if np.ndim(x) != 2:
			raise Exception("x must be 2D array")
		if np.size(x,1) != n:
			raise Exception("size(m,0) must equal size(x,1)")
		
		if np.ndim(z) != 1:
			raise Exception("z must be 1D array")
		
				
		if np.size(x,0) != p:
			print "x"
			print x
			print "m"
			print m
			raise Exception("size(x,0) must equal prod(m)")
		if np.size(z,0) != p:
			raise Exception("size(z,0) must equal prod(m)")
		
		A = np.zeros( (p,p) )
		Z = np.zeros( (p,1) )
		
		for a in range(0,p): # row
			for b in range(0,p): # col
				# i = array of power for each of the n variables
				i = index(b,m)
				A[a][b] = 1
				for c in range(0,n):
					A[a][b] *= pow( x[a][c], i[c] )
				Z[a] = z[a]
		
		
		try:
			B = np.linalg.solve(A,Z)
		except np.linalg.linalg.LinAlgError:
			print x
			#plt.plot(x[:,0],x[:,1],'o')
			#plt.show()
			raise Exception("singular matrix!")


			
		self.m = m
		self.n = n
		self.p = p
		self.B = B		
		
		#print "B",B
	##
	##
	def eval(self,x):
		#print "eval",x
		
		if np.ndim(x) != 2:
			raise Exception("x must be 2D array")
		
		q = np.size(x,0)
		
		if np.size(x,1) != self.n:
			raise Exception("size(x,1) must equal size(m,0)")
		
		z = np.zeros( q )

		for a in range(0,q): # data point
			z[a] = self.eval_single(x[a,:])
		
		return z
	##
	##
	def eval_single(self,x):
		#print "eval_single",x
		B = self.B
		
		#print "B",self.B

		if np.ndim(x) != 1:
			raise Exception("x must be 1D array")
		
		if np.size(x,0) != self.n:
			raise Exception("size(x,1) must equal size(m,0)")
		
		z = 0
		for b in range(0,self.p): # term
			i = index(b,self.m)
			#print "i",i
			y = 1
			#print "y",y
			for c in range(0,self.n): # variable
				y *= pow( x[c], i[c] )
			
			y *= self.B[b]

			#print "y",y
			z += y
			#print "z",z
		
		#print "B",self.B

		return z
	##
	##
	def eval_grad_single(self,x):
		print "eval_grad_single"
		
		if np.ndim(x) != 1:
			raise  Exception("x must be 1D array")
		
		if np.size(x,0) != self.n:
			raise Exception("size(x,0) must equal size(m,0)")
		
		g = np.zeros( self.n )
		
		for a in range(0,self.n): # component of gradient
			for b in range(0,self.p): # term
				i = index(b,self.m)
				y = 1

				#print "i",i
				#print "y",y

				for c in range(0,self.n): # variable
					if c == a:
						if i[c] == 0:
							y *= 1
						else:
							y *= i[c] * pow( x[c], i[c]-1 )
						
					else:
						y *= pow( x[c], i[c] )

					#print "y",y,"a",a,"c",c
					
				y *= self.B[b]
	
				#print "y",y

				g[a] += y
	

		if 0:
			print "x",x
			print "B",self.B
		
		return g








# sample data
#x = np.array([
#	[0,0],
#	[1,0],
#	[2,0],
#	[0,1],
#	[1,1],
#	[2,1]])
#
#z = np.array([1,2,3,4,5,6])

#s = spline( np.array([2,3]),x,z)

#z2 = s.eval(x)

#print z
#print z2



#plt.contourf(x,y,z)
#plt.show()

#print B

