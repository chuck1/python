import os
import math
import re
import sys
from lxml import etree
import numpy as np

modules_dir = os.environ["HOME"] + "/Programming/Python/Modules"
sys.path.append( modules_dir )

def volume_cuboid( root ):
	print "cuboid"
	
	x = float( root.find('x').text )
	y = float( root.find('y').text )
	z = float( root.find('z').text )
	
	print "{0:f} {1:f} {2:f}".format(x,y,z)
	
	return ( x*y*z )

def volume( root ):
	v = 0
	
	cuboids = root.findall('cuboid')
	for c in cuboids:
		v += volume_cuboid( c )
	
	return v

