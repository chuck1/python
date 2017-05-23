from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import random as rd
import numpy as np

def gen_index(a,n):
	d = np.size(n,0)
	i = np.zeros(d)
	
        b = a
        i[0] = b % n[0]
        for c in range(1,d):
                b = ( b - i[c-1] ) / n[c-1]
                i[c] = b % n[c]
        return i


class dfs:
	def __init__(self,n):
		self.n = n
		self.d = len(n)
		self.N = np.prod(n)
		self.ispath = np.zeros(self.N)
		self.dead = np.zeros(self.N)
		self.unvisited = np.ones(self.N)
		self.visited0 = np.zeros(self.N)
		self.visited1 = np.zeros(self.N)

		
	def flat(self,i):
		a = 0
		s = 1
		for c in range(0,self.d):
			a += i[c] * s
			s *= self.n[c]
		return a

	def index(self,a):
	        i = np.zeros(self.d)
		
	        b = a
	        i[0] = b % self.n[0]
	        for c in range(1,self.d):
	                b = ( b - i[c-1] ) / self.n[c-1]
	                i[c] = b % self.n[c]
	        return i

	def span(self,a):
		i = self.index(a)
		span = np.zeros( (self.d,2), int )
		for c in range(self.d):
			if i[c] > 0:
				span[c,0] = -1
			
			if i[c] < (self.n[c]-1):
				span[c,1] = 1
		return span

	def stencil(self,a,s):
		i = self.index(a)
		adj = np.array([],int)
		m = np.ptp( s, axis=1 ) + 1
		n = np.prod( m )
	
		#print "m"
		#print m	
		#print "span"
		#print s
			
		perm = np.zeros( (n,self.d) )
		
		for p in range(n):
			k = gen_index( p, m )
			for c in range(self.d):
				perm[p,c] = s[c,0] + k[c]

		#print "perm"
		#print perm

		for p in range(n):	
			j = np.array(i)
			j += perm[p,:]
			#if np.all(i==j) == 0:
			adj = np.append( adj, int( self.flat(j) ) )
		
		return adj
		
		
	
	def adjacent(self,a):
		i = self.index(a)
		adj = np.array([],int)
		for c in range(self.d):
			if i[c] > 0:
				j = np.array(i)
				j[c] -= 1
				adj = np.append( adj, int( self.flat(j) ) )
			if i[c] < (self.n[c]-1):
				j = np.array(i)
				j[c] += 1
				adj = np.append( adj, int( self.flat(j) ) )
		return adj
		
	def vha(self):
		for a in range(0,self.N):
			if self.unvisited[a]:
				count = 0
				for adj in self.adjacent(a):
					if self.ispath[adj]:
						count += 1
				if count > 1:
					self.unvisited[a] = 0
					self.visited0[a] = 1
			
			if self.unvisited[a]:
				s = self.span(a)
			
				sten = self.stencil(a,s)
				
				X = np.array( self.ispath )
				X = X[ sten ]
				
				shp = np.ptp(s,axis=1) + 1
	
				Y = np.reshape( X, tuple( shp ), order='F' )
				
				count = 0
				for c in range(self.d):
					
					
					Z = np.array(Y)
					for e in range(self.d-1,-1,-1):
						if e != c:
							Z = np.any( Z, axis=e )
					
					if np.sum( Z ) > 1:
						count += 1
					
				if count > 1:
					self.unvisited[a] = 0
					self.visited1[a] = 1
				
					if 1:
						print "span"
						print s
						print "sten"
						print sten
						print "X"
						print X
						print "Y"
						print Y
						print "shape"
						print shp



			
	def rand_select(self,a):
		adj = self.adjacent(a)
		u = self.unvisited[ adj ]
		adj = adj [ u == 1 ]
		if np.size(adj,0) > 0:
			return adj[ rd.randrange( np.size(adj,0) ) ]
		else:
			return -1
	
	def backtrack(self,a):
		while 1:
			self.dead[a] = 1
			progress = 0
			for adj in self.adjacent(a):
				if (self.ispath[adj]==1) & (self.dead[adj]==0):
					progress = 1
					
					b = self.rand_select(adj)
					if b != -1:
						return b
					
					a = adj
					break
			
			if progress == 0:
				return -1
	
	def run(self):
		print "running..."
		a = 0
		while 1:
			self.ispath[a] = 1
			self.unvisited[a] = 0

			print np.sum( self.unvisited )

			self.vha()
		
			#print np.reshape( self.ispath, tuple(self.n) )
	
			b = self.rand_select(a)
			if b == -1:
				c = self.backtrack(a)
				if c == -1:
					break
				else:
					a = c
					continue
			else:
				a = b
				continue		
	
	def ploting(self,V):
		ind = np.argwhere( V == 1 )
		n = np.size( ind, 0 )
		x = np.zeros( (n,self.d) )
		for b in range(n):
			x[b,:] = self.index( ind[b] )
			
		if self.d == 3:
		
			
			fig = plt.figure()
			#ax = fig.add_subplot(111, projection='3d')
			ax = Axes3D(fig)
			ax.scatter( x[:,0], x[:,1], x[:,2] )
			
			for b in range(n):
				W = np.zeros((2,2,3))
				X = np.zeros((2,2))
				Y = np.zeros((2,2))
				Z = np.zeros((2,2))
				for l in range(3):	
					for i in range(2):
						for j in range(2):
							for k in range(2):
								ind = np.array([i,j,k])
								#W[j,k,(l+0)%3] = x[b,(l+0)%3] + ind[(l+0)%3] - 0.5
								#W[j,k,(l+1)%3] = x[b,(l+1)%3] + ind[(l+1)%3] - 0.5
								#W[j,k,(l+2)%3] = x[b,(l+2)%3] + ind[(l+2)%3] - 0.5
								W[j,k,0] = x[b,0] + ind[(l+0)%3] - 0.5
								W[j,k,1] = x[b,1] + ind[(l+1)%3] - 0.5
								W[j,k,2] = x[b,2] + ind[(l+2)%3] - 0.5

								
						X = W[:,:,0]
						Y = W[:,:,1]
						Z = W[:,:,2]
						ax.plot_surface(X,Y,Z)
				
			#plt.show()
		
		if self.d == 2:
			x = np.reshape( V, tuple(self.n) )
			plt.figure()
			plt.imshow( x, cmap=plt.cm.gray, interpolation='nearest' )
			#plt.show()
		




n = 12

m = dfs( np.array((n,n)) )

m.run()


m.ploting(m.ispath)
m.ploting(m.visited0)
m.ploting(m.visited1)

plt.show()














