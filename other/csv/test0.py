#!/usr/bin/env python

import sys
import numpy as np
import matplotlib.pyplot as plt
import csv



def measure():	
	r = 0
	with open(sys.argv[1]) as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			r += 1
	
	
	
	print "{0} rows".format(r)


	
def extract():
	rows = int(sys.argv[2])
	cols = int(sys.argv[3])
	
	data = np.zeros((rows,cols))
	
	r = 0
	with open(sys.argv[1]) as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			for c in range(cols):
				data[r,c] = float(row[c])
			r += 1
	
	
	print np.shape(data)
	print data
	
	
	y = data[:,0]
	z = data[:,1]
	w = data[:,2]
	
	#plt.plot(y,z,'o')
	

	ind = (w > 0)
	data = data[ind,:]
	y = data[:,0]
	z = data[:,1]
	w = data[:,2]

	

	ind = (y == -0.00025)
	
	data = data[ind,:]
	
	y = data[:,0]
	z = data[:,1]
	w = data[:,2]

	#plt.plot(y,z,'o')
	#plt.show()
	
	t = 0.0135
	r = 0.0002
	
	ind = (z >= (t-r)) & (z <= (t+r))
	
	data = data[ind,:]
	
	y = data[:,0]
	z = data[:,1]
	w = data[:,2]

	print "at z = {0}, average w = {1}".format(t,np.mean(w))

	plt.plot(z,w,'o')
	plt.show()
	
	
	#plt.xlim([-0.01,0.01])
	
	#plt.xlabel('x (m)')
	#plt.ylabel('heat flux (W/m2)')
	
		
if len(sys.argv) == 2:
	measure()

if len(sys.argv) == 4:
	extract()



