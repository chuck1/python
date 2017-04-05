import pylab as pl
import numpy as np
import math


def ttrow(i, d, n):
	#print "i",i,"d",d,"n",n
	
	a = np.zeros(n)
	for j in range(n):
		if j >= d:
			den = math.factorial(j-d)
			#print den
			a[j] = i**(j-d) / den

	
	#print "a",a
	
	return a


def tt(i,d):
	# APPLIES TO UNIFORM GRID
	# i is the index or location
	# d is the orderof the term
	# X is a coefficient of the terms not including the first
	# the coefficnet of the first term is one
	
	m = len(i)
	n = m-1
	
	#T = sym(zeros(m,n))
	T = np.zeros((m,n))
	
	for j in range(m):
		T[j,:] = ttrow(i[j],d[j],n)
	
	
	
	A = np.transpose(T[1:m,0:m-1])
	
	b = -T[0,0:m-1]
	b = np.reshape(b, (1,n))
	b = np.transpose(b)
	
	ver = False
	if ver:
		print "m",m,"n",n
		print "T"
		print T
		print "A"
		print A
		print "b"
		print b
	
	X = np.dot(np.linalg.inv(A), b)
	
	#print "i",i
	#print "d",d
	#print "X"
	#print X
	
	return X
	
def freq(B,P,A,h,k,b0,p0):
	
	A = np.reshape(A,np.size(A,0))
	A = -A

	N = 0
	D = 1

	#print "b0",b0,"p0",p0
	
	for b,p,a in zip(B,P,A):
		
		if p < p0:
			b = float(b - b0)
			p = float(p - p0)
			#print "b",b,"p",p,"a",a
		
			N += a * np.exp(1j * k * h * b) * np.power(1j * h * k, p)
		elif p == p0:
			b = float(b - b0)
			D += a * np.exp(1j * k * h * b)
		else:
			raise ValueError('derivative too high')
		
	H = N/D
		
	return H

def freqs(B,P):
	
	h = 0.01
	k = np.linspace(1,10,100)

	fig = pl.figure()
	ax0 = fig.add_subplot(111)
	fig = pl.figure()
	ax1 = fig.add_subplot(111)
	
	for b,p in zip(B,P):
		A = tt(b,p)
		
		H = freq(b[1:], p[1:], A, h, k, b[0], p[0])
	
		ax0.plot(k,np.real(H))
		ax1.plot(k,np.imag(H))
	
	
	ax0.legend(range(len(B)))
	ax1.legend(range(len(B)))

	pl.show()

	
	
#i = [0 0 1 2 0];
#d = [1 0 0 0 3];

#i = [0, 0, -1]
#d = [1, 0,  0]

#i = [0, -1, -2, -1, 0]
#d = [1,  1,  0,  0, 0]

#i = [0, -1, -3, -2, -1, 0]
#d = [1,  1,  0,  0,  0, 0]

B = [
		[0, 0, -1],
		[0, 0, -1, -2, -3],
		[0, 0, -1, -2, -3, -4, -5, -1, -2, -3]]

P = [
		[1, 0, 0],
		[1, 0, 0, 0, 0],
		[1, 0, 0, 0, 0, 0, 0, 1, 1, 1]]

freqs(B,P)


