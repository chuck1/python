#!/usr/bin/env python

import sys
import os
import numpy as np
import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

module_dir = os.environ["HOME"] + "/Programming/Python/Modules/"
sys.path.append(module_dir)

import CSV
import commandline as cl
import data_analysis as da

tol = 1e-7

def zoom(data,ind,a,b):
	x = data[:,ind]
	
	data = data[np.logical_and(x>a,x<b),:]
	
	return data

if __name__ == "__main__":

	if len(sys.argv) < 2:
		print "Usage: {0} FILENAME [OPTIONS...]".format(sys.argv[0])
		sys.exit(0)
	
	c = cl.commandline(sys.argv,{
		'x':cl.Arg('x'),
		'y':cl.Arg('y'),
		'z':cl.Arg('z'),
		'delim':cl.Arg('d')})
	
	filename = c.free[0]
	
	if len(c.args['delim'].values) > 0:
		delim = (c.args['delim'].values[0]).decode('string_escape')
	else:
		delim = ','

	xind = c.args['x'].values[0]
	yind = c.args['y'].values[0]
	zind = c.args['z'].values[0]

	
	# program
	
	#print "delim='{0}'".format(delim)
	
	data = CSV.read(filename, delim)


	print np.shape(data)
	
	yzoom = -2.165e-4
	
	data = zoom(data,yind,yzoom-tol,yzoom+tol)

	x = data[:,xind]
	y = data[:,yind]
	z = data[:,zind]

	print np.shape(data)

	#fig0 = plt.figure()
	fig1 = plt.figure()
	fig2 = plt.figure()
	
	#ax0 = Axes3D(fig0)
	ax1 = fig1.add_subplot(111)
	ax2 = fig2.add_subplot(111)

	
	#ax0.plot(data[:,1],data[:,2],data[:,3],'o')

	ax1.plot(z,data[:,3],'o')
	ax2.plot(z,data[:,4],'o')

	
	plt.show()








