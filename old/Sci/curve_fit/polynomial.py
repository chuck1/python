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

def fit(ax,x,y,d):
	z = np.polyfit(x,y,d)
	print z
	p = np.poly1d(z)
	
	ax.plot(x,y,'o')
	
	x0 = np.linspace(x[0],x[-1],100)
	ax.plot(x,p(x),'-')


if __name__ == "__main__":
	
	if len(sys.argv) < 2:
		print "Usage: {0} FILENAME [DELIMITER]".format(sys.argv[0])
		sys.exit(0)
	
	filename = sys.argv[1]
	
	if len(sys.argv) > 2:
		delim = (sys.argv[2]).decode('string_escape')
	else:
		delim = ','


	data = CSV.read(filename, delim)
	
	print data
	print np.shape(data)
	
	fig = plt.figure()
	ax = fig.add_subplot(111)
	
	X = [data[0:7,0],data[6:8,0],data[7:,0]]
	Y = [data[0:7,1],data[6:8,1],data[7:,1]]
	
	
	fit(ax,X[0],Y[0],3)
	fit(ax,X[1],Y[1],1)
	fit(ax,X[2],Y[2],3)


	plt.show()
