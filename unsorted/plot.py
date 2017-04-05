#!/usr/bin/env python

import sys
import os
import numpy as np
import csv
import matplotlib.pyplot as plt

module_dir = os.environ["HOME"] + "/Programming/Python/Modules/"
sys.path.append(module_dir)

import CSV
import commandline as cl

def myplot():
	if len(sys.argv) == 1:
		print "Usage: {0} FILENAME [OPTIONS...]".format(sys.argv[0])
		sys.exit(0)

	c = cl.commandline(sys.argv,{'x':cl.Arg('x'),'y':cl.Arg('y'),'delim':cl.Arg('d')})


	filename = c.free[0]
	
	if len(c.args['delim'].values) > 0:
                delim = (c.args['delim'].values[0]).decode('string_escape')
        else:
                delim = ','

	
	xind = c.args['x'].values
	yind = c.args['y'].values
	
	print xind
	print yind
	
	print "delim='{0}'".format(delim)
	
	
	data = CSV.read(filename, delim)

	print data
	print np.shape(data)
	
	for xi in xind:
		fig = plt.figure()
		ax = fig.add_subplot(111)
		for yi in yind:
			ax.plot(data[:,xi],data[:,yi],'o')
	
	#for i in range(0,np.size(data,1)):
	#	plt.semilogy(data[:,i])
	
	plt.show()
