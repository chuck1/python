import numpy as np
import math

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-p',action='store_true')
args = parser.parse_args()

if args.p:
    import pylab as pl

def linear(x1,x2,y1,y2):
	m = (y2-y1)/(x2-x1)
	b = y2 - m * x2
	x = -b / m
	return x

def log(x1,x2,y1,y2):
	
	m = (np.log(y2) - np.log(y1)) / (np.log(x2) - np.log(x1))
	b = np.log(y2) - m * np.log(x2)
	x = (np.log(goal) - b) / m
	return np.exp(x)
	
	

# @param x array with two values for initial guess
# @param f function f(x)=0
def shooting(obj,x,f):
	print "shooting method"
	
	# x[0] and x[1] are the two initial guesses

	print "x",x
	print "f",f
	
	X = np.array(x)
	
	#print np.shape(X)
	#print np.shape(X[0])
	
	

	Y = np.zeros((2,))
	
	while True:

		try:
			Y[0] = f(obj,X[0])
		except ValueError:
			Y[0] = float('NaN')
	
		try:
			Y[1] = f(obj,X[1])
		except ValueError:
			Y[1] = float('NaN')
	
		if(np.all(np.isnan(Y))):
			raise ValueError()
	
		if(math.isnan(Y[0])):
			print "f({0}) = nan. trying new X[0].".format(X[0])
			X[0] = (X[0] + X[1]) / 2.0
			continue
		
		if(math.isnan(Y[1])):
			print "f({0}) = nan. trying new X[1].".format(X[1])
			X[1] = (X[0] + X[1]) / 2.0
			continue
		
		break
	
	#print "X",X
	#print "Y",Y
	#print "loop"

	i = 0
	j = 1
	
	for a in range(10):
		
		xn = linear(X[j], X[i], Y[j], Y[i])
		
		try:
			yn = f(obj,xn)
		except ValueError:
			yn = nan


		"""
		if xn < 0:
			break
		if math.isinf(xn):
			break
		if math.isinf(yn):
			break
		"""
		
		def plot():
			if args.p:
				print X
				print Y
				pl.plot(X,Y,'o')
				pl.loglog(X,Y,'o')
				pl.show()
		#plot()
	
		
		print "X",X,np.shape(X)
		print "Y",Y,np.shape(Y)
		print "xn {0:e}".format(xn),np.shape(xn)
		print "yn {0:e}".format(yn),np.shape(yn)
		
		#X = np.append(X, np.reshape(xn, (1,) + np.shape(xn)), 0)
		X = np.append(X, np.reshape(xn, (1,) + np.shape(xn)), 0)
		#Y = np.append(Y, np.reshape(yn, (1,) + np.shape(yn)), 0)
		Y = np.append(Y, np.reshape(yn, (1,)), 0)

		if(np.all(np.fabs(Y[-1]) < 1.0)):
			break
		
		#d1 = math.fabs(X[-1] - X[j])
		#d2 = math.fabs(X[-1] - X[i])
		
		#if(d1 < d2):
		#	i = j
		#else:
		#	i = i

		i = j
		j = j + 1
	

	
	#i = x > 0
	#x = x[i]
	#y = y[i]

	#print x
	#print y

	#y = y + 1e5

	def plot():
		if args.p:
			pl.plot(X,Y,'o')
			#pl.loglog(X,Y,'o')
			pl.show()
	plot()

	#print X

	return X[-1]












