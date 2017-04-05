#!/usr/bin/env python

import re
import os
import sys
import math
import numpy as np
import lxml.etree as etree
import logging
import matplotlib.pyplot as plt

modules_dir = os.environ["HOME"] + "/Programming/Python/Modules"
sys.path.append( modules_dir )

import plot
import Sci.Geo as Geo
import XML

logging.basicConfig(level=logging.DEBUG)

def extract2( f, find_str, ext_str, offset ):
	find_pat = re.compile( find_str )
	ext_pat = re.compile( ext_str )
	
	found = 0
	offset -= 1
	
	for line in open(f, 'r'):
		# print 'line=%r' % line
		if found:
			if offset == 0:
				print "extract line=%r" % line
				return ext_pat.match(line)
			else:
				offset -= 1
		else:
			m = find_pat.match(line)
			# print 'found=0,m=',m
			if m:
				found = 1

	print "reached EOF"
	return None

def extract( str_search, str_pattern, str_filename ):
	# pattern = re.compile(".*\s([\w-]+)\s+(-?[\w\.]+)\s.*");
	pattern = re.compile( str_pattern )
	
	ret = ""
	
	for line in open( str_filename, 'r' ):
		if re.search( str_search, line ):
			# print 'line=%r' % line
			if line == None:
				print 'no matches found'
			else:
				m = pattern.match(line)
				if m:
					return m.group(1)
				else:
					raise Exception( "no match for %r in %r" % (str_pattern, line) )

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

def grid_refinement(phi,n,ax0):
	# make sure r > 1
	
	h = np.power( v/n, 1.0/3.0 )
	
	arg = np.argsort(h)
	
	phi = phi[arg]
	n = n[arg]
	h = h[arg]
	
	
	e21 = phi[1] - phi[0]
	e32 = phi[2] - phi[1]
	r21 = float(h[1]) / float(h[0])
	r32 = float(h[2]) / float(h[1])
	
	p = [1]
	
	print "phi={0}".format(phi)
	print "n  =",n
	print "h  =",h

	print "r21=",r21
	print "r32=",r32
	print "e21=",e21
	print "e32=",e32
	
	a = math.log( math.fabs(e32/e21) )
	e = math.copysign(1,e32/e21)
	
	i = 0
	while 1:
		p.append(p[-1])
		#pold = p
		
		
		c = math.pow(r21,p[-1]) - e
		d = math.pow(r32,p[-1]) - e
		b = math.log(c/d)
		
		p[-1] = 1 / math.log(r21) * math.fabs( a + b )
		
		if p[-1] == 0 and p[-2] == 0:
			break
		
		if ( math.fabs( (p[-1] - p[-2])/p[-2] ) < 0.0001 ):
			break

	#plt.plot(p,'-o')
	#plt.show()

	
	gci = math.fabs( ( phi[0] - phi[1] )/( 1 - math.pow(r21, p[-1]) ) )
	
	err = np.abs(gci/phi)
	
	err_tar = 0.03

	gci_tar = math.fabs(err_tar * phi[0])
	
	h_tar = h[0] * math.pow(gci_tar / gci, 1.0 / p[-1])
	
	if h_tar > 0:
		n_tar = v / math.pow(h_tar,3)
	
	plot.plot(ax0, h, phi)
	
	print
	print "gci:        {0}".format(gci)
	print "percent err:{0}".format(err*100)
	print "p:          {0}".format(p)
	print "err_tar:    {0}".format(err_tar)
	print "gci_tar:    {0}".format(gci_tar)
	print "h_tar:      {0}".format(h_tar)
	print "n_tar:      {0} million".format(n_tar/1.0e6)


def grid_refinement_pre(value_string,ax0):
	print "value_string = {0}".format(value_string)
	
	phi = np.zeros(len(dirs))
	n = np.zeros(len(dirs))
	
	for i, dir in dirs:
		val_str = ['exp','out','case{{id={0:d}}}'.format(i),'val{{name={0:s}}}'.format(value_string)]
	
		val = XML.find(root, val_str, True )
	
		if val.text is None:
			print "val node for case {0} does not exist".format(i)
			sys.exit(0)
		
		phi[i] = float(val.text)
		
		filename_log = folder + dir + "/job.log"
		
		# extract number of grid cells from file
		res = extract2(filename_log, 'Mesh Size', '^\s*([0-9]+)\s+([0-9]+).*$', 3)
	
		if res is None:
			print "res is None"
			sys.exit(0)
		
		if res.group(2) is None:
			print "Mesh Size not found"
			sys.exit(0)
		
		n[i] = int( res.group(2) )
		
	
	
	print "volume = %10e" % v
	
	
	
	grid_refinement(phi,n,ax0)
	
	

####################################################################

# this program calculates the GCI for a grid refinement study
# <folder> should contain folders named case_X where X is 0, 1, and 2

if len( sys.argv ) < 3:
	print "usage: %r FOLDER VALUE..."%sys.argv[0]
	sys.exit(0)

folder = sys.argv[1]

value_strings = []

for i in range(2,len(sys.argv)):
	value_strings.append(sys.argv[i])

# ----------------------------------------------------------------

fig = plt.figure()
ax = fig.add_axes([0.1,0.1,0.8,0.8])

xmlfilename = folder + "exp.xml"

tree = etree.parse( xmlfilename )
root = tree.getroot()

v = Geo.volume( root.find('geo') )

#print "v={0:e}".format(v)

dirs = indexed_directories(folder,"case_(\d+)")

for str in value_strings:
	grid_refinement_pre(str,ax)

ax.set_xlabel("grid size (m)")
ax.set_ylabel("temperature gradient (K/m)")

ax.legend(value_strings, loc="best")


plt.show()

