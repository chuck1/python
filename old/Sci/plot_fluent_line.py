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

if __name__ == "__main__":
	
	c = cl.commandline(sys.argv,{
		'origin':cl.Arg(''),
		'delim':cl.Arg(''),
		'dir':cl.Arg('')
		})
	
	#if len(sys.argv) < 2:
	#	print "Usage: {0} FILENAME [DELIMITER]".format(sys.argv[0])
	#	sys.exit(0)
	
	filename = c.free[0]
	
	if len(c.args['delim'].values) > 0:
		delim = (c.args['delim'].values[0]).decode('string_escape')
	else:
		delim = ','
	
	dir = np.array([float(f) for f in c.args['dir'].values])
	
	origin = np.array([float(f) for f in c.args['origin'].values])
	
	print dir
	print origin	
	
	
	# program
	
	#print "delim='{0}'".format(delim)
	
	data = CSV.read(filename, delim)

	print data
	print np.shape(data)

	data, arg, r = da.all_in_direction(origin, dir, data, [1,2,3], True)
	
	
	
	print data
	print np.shape(data)

	fig0 = plt.figure()
	fig1 = plt.figure()

	ax0 = Axes3D(fig0)
	ax1 = fig1.add_subplot(111)
	
	ax0.plot(data[:,1],data[:,2],data[:,3],'o')
	ax1.plot(data[:,3],data[:,4],'o')
	
	plt.show()








