#!/usr/bin/env python

import itertools
import sys
import math
#import time
import os
import re
import numpy as np

import matplotlib.pyplot as plt
#import matplotlib as mpl

from lxml import etree

modules_dir = os.environ["HOME"] + "/Programming/Python/Modules"
sys.path.append( modules_dir )

import plot as plot
import cluster
import data_analysis as DA
import CSV
import XML
import interpolation2 as i2
#import vector

def argnearest(array, value):
	index = (np.abs(array-value)).argmin()
	return index

def nearest(array, value):
	return array[argnearest(array, value)]

def my_formatter_func(x, p):
	return "{0:0.1e}".format(x)
	

def indexed_directories(path,str):
        dir = []

        pat = re.compile(str)

        walk = os.walk(path)
        for path, dirs, files in walk:
                print path, dirs, files
                for d in dirs:
                        s = pat.match(d)
                        if s:
                                dir.append( (int(s.group(1)), d) )
                break

        dir = sorted(dir, key=lambda d: d[1])

        return dir


def sub_process(id_case, dir, str_value, x, y, z, direction, verbose_plot, ax):
	filename_data = folder + dir + "/out/interior.csv.out"
	
	print "file={0:s}".format(filename_data)
	
	# ------------------------------------
	
	#int(re.search("case\_(\d+)", dir).group(1))
	
	# ----------------------------------------
	z_ind = 3
	z_index = 3
	
	tol = 1e-7
	
	tol_init = 1e-6
	

	
	# get data
	
	sys.stdout.write("converting csv file to numpy array...")
	sys.stdout.flush()
	
	data = CSV.read(filename_data)
	
	sys.stdout.write(" returned {0} array\n".format(np.shape(data)))
	
	if np.size(data,0)==0:
		sys.exit(0)
	
	# take z-slice ---------------------------------------------------------------------
	z_unique = np.unique( data[:,z_index] )
	z = nearest(z_unique, z)
	
	
	sys.stdout.write("taking z-slice...")
	sys.stdout.flush()
	
	data = data[ ( data[:,z_ind] < ( z+tol_init ) ) & ( data[:,z_ind] > ( z-tol_init ) ), : ]
	
	sys.stdout.write(" returned {0} array\n".format(np.shape(data)))
	
	 
	
	#clus = cluster.clusters1D( data[:,z_ind], 1e-6 )
	#clu = clus.closest_to( z )
	#data = data[ clu.arg, : ]
	#print "shape(data)", np.shape(data)
	
	#print_data( data )
	
	# find nearest points along a line ---------------------------------------------------
	
	# interp stencil
	m = np.array([4])
	# interp variable column index
	i = np.array([1,2])
	# temperature column index
	j = 4
	# direction
	#dir = np.array([0,1])
	
	arg,r = DA.nearest_in_direction( np.array([x,y]), data[:,i], m[0], direction[0:2] )
	
	#print np.shape(r)
	#print r
	
	
	
	# --------------------------------------------
	
	s = i2.spline( m, r, data[arg,j] )
	grad = s.eval_grad_single( np.array([0]) )
	grad = grad[0]

	if direction[1]>0:
		grad = -grad
	
	
	#print grad
	
	print "output_gradient %e" % grad
	
	
	plot.plot(ax,r,data[arg,j])

	if verbose_plot:
		plot.print_data2(data,arg)

	
	
	
	#cond = 16
	#flux = -cond * grad
	#print "flux %e" % flux
	
	# append xml for experiment ----------------------------------
	
	
	str = [
		"exp",
		"out",
		"case{{id={0:d}}}".format(id_case),
		"val{{name={0:s}}}".format(str_value)]
	
	element = XML.find(root, str, True)
	
	element.text = "{0:e}".format(grad)
	
	print element
	


# ------------------------------------------
usage = "usage: python {0:s} <folder> <val_name>".format(sys.argv[0])

if len(sys.argv) < 3:
	print usage
	sys.exit(1)

folder = sys.argv[1]

strings_value = []
for i in range(2,len(sys.argv)):
	strings_value.append(sys.argv[i])

#-------------------------------
dirs = indexed_directories(folder,"case_(\d+)");

print dirs

# get x, y, z from experiment's xml file
filename_xml = folder + "exp.xml"

tree = etree.parse(filename_xml)
root = XML.Element(tree.getroot())

for val_name in strings_value:
	
	# origin
	str = [
		"exp",
		"post",
		"{0:s}".format(val_name),
		"o"]
	
	element_origin = XML.find(root, str, False)
	
	if element_origin is None:
		print "not found"
		sys.exit(1)
	
	if element_origin.text is None:
		print "not found"
		sys.exit(1)
	
	search = re.findall('[-e\.\d]+', element_origin.text)
	
	print search
	
	x = float(search[0])
	y = float(search[1])
	z = float(search[2])

	# direction
	str = [
		"exp",
		"post",
		"{0:s}".format(val_name),
		"d"]
	
	element_origin = XML.find(root, str, False)

	element_origin
	
	
	search = re.findall('[-e\.\d]+', element_origin.text)
	
	print search
	
	dx = float(search[0])
	dy = float(search[1])
	dz = float(search[2])
	
	direction = np.array([dx,dy,dz])

	print "direction = ",direction[0:2]
	
	print "xyz=",x,y,z
	
	# process
	
	ax = plt.axes()
	
	for i, dir in dirs:
		sub_process(i,dir,val_name, x, y, z, direction, False, ax)
	
	plt.show()
	
	
tree.write(filename_xml)






