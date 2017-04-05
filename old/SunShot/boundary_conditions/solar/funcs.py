#!/usr/bin/env python

import sys, os
import numpy as np
import math
import scipy.optimize

module_dir = os.environ["HOME"] + "/Documents/Programming/Python/Modules/"
sys.path.append(module_dir)

import csv

import argparse


# a*(x*x + y*y) + b*(x + y) + c

def fun1(p, x, y, x0 = 0.0, y0 = 0.0):
        return p[0] * np.exp(p[1] * (x**2 + y**2))


# centered normal distribution
	

# non-centered normal distribution
def fun2(p, x):
	return p[0] * np.exp(p[1] * (x - p[2])**2)

def errfun2(p, r, f):
	return f - fun2(p, r)


# centered normal distribution
def fun3(p, r):
	return p[0] * np.exp(p[1] * r**2)

def fun3xy(x, y, x0, y0, p):
	r = np.sqrt(np.square(x - x0) + np.square(y - y0))
	return fun3(p, r)



def fun_grid(fun, x, y, n, xc, yc, *args):
	x = np.linspace(x[0], x[1], n)
	y = np.linspace(y[0], y[1], n)
	
	#print x
	#print y

	X,Y = np.meshgrid(x,y)
	
	F = fun(X,Y,xc,yc,args)
	
	return X,Y,F



def numerically_integrate_2D(p,fun, x, y):
	# equation:
	# f = a * exp(b * x**2)
	# a and b are constants
	# x is distance from center
	
	res = 0.01
	
	n = 100
	
	l = x[1] - x[0]
	w = y[1] - y[0]

	A = l * w
	
	A_cell = (l/float(n-1)) * (w/float(n-1))
	
	X,Y,F = fun_grid(p, fun, x, y, n)

	FA = F * A_cell
	
	def plot():
		CS = plt.contourf(X,Y,F)
		CB = plt.colorbar(CS,format='%e')
		CB.set_label('heat flux (W/m2)')
		plt.axis('equal')
		plt.show()
	
	#plot()
	
	aa = np.sum(FA) / A
	#print "area average = {0:e}".format(aa)
	return aa
	
def fun(x,a,b):
	y = a*x*x + b
	return y

def integrate_poly2d(w, p):
	o = np.size(p,0)
	
	n = np.arange(o)[::-1]
	
	w = np.ones(o) * w
	
	print
	print
	
	z = 2 * p / (n+1) * np.power(w,n+2) 

	print p
	print n
	print w
	print z

	z = np.sum(z)
	
	print z
	
	# int 0 w int 0 w    a * (x^n) * dx * dy
	
	# 2 * a / (n+1) * w^(n+1) * w
	# 2 * a / (n+1) * w^(n+2)
	
	# n = 0
	# 2 * a * w^2
	
        return z

def scale( S, w, p):
	S0 = integrate_poly2d(w, p)
	
	
	
	c = ( S - S0 ) / w / w / 2
	
        return c
	
def parab_2d_coeff_from_meas( peak, edge, edge_x ):
	a = ( edge - peak ) / edge_x / edge_x
	
        return a

def plot2d(filename,a,c):
	
	data = np.zeros((40,2))
	
	r = 0
	with open(filename) as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			data[r,0] = float(row[0]) * 0.001
			data[r,1] = float(row[1]) * 10000
			r += 1
	
	print np.shape(data)
	print data
	
	x = data[0:15,0] - 0.005
	y = data[0:15,1]
	
	plt.plot(x,y,'o')
	
	x = data[15:30,0] - 0.005
	y = data[15:30,1]
	
	plt.plot(x,y,'s')
	
	plt.plot(x,fun(x,a,c))

	plt.xlabel('x (m)')
	plt.ylabel('heat flux (W/m2)')
	
	plt.show()
	
def get_csv_data(filename):
	raw = []
	with open(filename, 'r') as csvfile:
		spamreader = csv.reader(csvfile) 
		for row in spamreader:
			raw.append(list(float(c) for c in row))
	
	data = np.array(raw)
	
	return data

