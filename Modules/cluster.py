from matplotlib import pyplot as plt
import sys
import math
import numpy as np

class clust1D:
	def __init__( self, arg ):
		self.arg = np.array([arg])
		self.alive = 1
	def front( self ):
		return self.arg[0]
	def back( self ):
		return self.arg[ np.size( self.arg, 0 ) - 1 ]
	def append( self, clu ):
		self.arg = np.append( self.arg, clu.arg )
	def prnt( self ):
		print self.arg

class clusters1D:
	def __init__( self, data, dist_crit ):
		#print "init"
		self.data = data
		self.data_len = np.size( data, 0 )
		self.dist_crit = dist_crit
		
		self.arg = np.argsort( self.data )
		
		self.clusters = []
				
		for a in range( self.data_len ):
			self.clusters.append( clust1D( self.arg[a] ) )
		

		while self.count_alive() > 1:
			#print "loop"

			c_alive = self.count_alive()
			#print "c_alive",c_alive

			clust_arg = self.arg_alive()
			
			#print "clust_arg",clust_arg
			
			d = np.zeros( c_alive - 1 )
			
			# find closest living pair
			for a in range( 0, c_alive - 1 ):
				d[a] = self.dist( clust_arg[a], clust_arg[a+1] )	
			#print "d",d
			
			a = np.argmin(d)
			b = a + 1
			
			#print "a",a,"b",b
			
			# combine closest pair
			self.clusters[clust_arg[a]].append( self.clusters[clust_arg[b]] )
			
			self.clusters.pop(clust_arg[b])
			
			# kill clusters
			self.kill()

	def kill( self ):
		for a in range(len(self.clusters)):
			kill = 1
			if a < ( len(self.clusters) - 1 ):
				if ( self.dist( a, a+1 ) < self.dist_crit ):
					kill = 0
			if a > 0:
				if ( self.dist( a, a-1 ) < self.dist_crit ):
					kill = 0
			
			if kill==1:
				#print "kill %i" % a
				self.clusters[a].alive = 0
	
	
	def dist( self, a, b ):
		if a < b:
			return math.fabs( self.data[self.clusters[a].back()] - self.data[self.clusters[b].front() ] )
		elif a > b:
			return self.dist( b, a )
		elif a == b:
			raise Exception("a==b")

	def range( self, a ):
		return math.fabs( self.data[ self.clusters[a].front() ] - self.data[ self.clusters[a].back() ] )
		

	def plot( self ):
		for a in range( len( self.clusters ) ):
			clu = self.clusters[a]
			arg = clu.arg
			plt.plot( [a]*np.size(arg), self.data[arg],'o')
		plt.show()
	def prnt( self ):
		for a in range( len( self.clusters ) ):
			clu = self.clusters[a]
			arg = clu.arg
			print self.data[arg]
	def count_alive( self ):
		count = 0
		
		for c in self.clusters:
			count += c.alive

		return count
	def arg_alive( self ):
		arg = np.array( [], int )

		for a in range( len( self.clusters ) ):
			if self.clusters[a].alive:
				arg = np.append( arg, a )

		return arg
	def closest_to( self, x ):
		cc = len( self.clusters )
		d = np.zeros( cc )
		
		for a in range( cc ):
			df = math.fabs( self.data[ self.clusters[a].front() ] - x )
			db = math.fabs( self.data[ self.clusters[a].back() ] - x )
			d[a] = min( df, db )
		
		a = np.argmin( d )
		
		return self.clusters[a]
	
	
	

def test_cluster1D():
	data = np.random.rand(10)
	print data
	clu = clusters1D( data )
	clu.plot()
	for c in c.clusters:
		c.prnt()



