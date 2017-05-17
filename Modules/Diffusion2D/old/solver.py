import time
import numpy as np
import itertools
import pylab as pl
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import math
import inspect
import pickle
import signal
import sys

from unit_vec import *
from Prob import *
from Face import *
from Util import *

	
def load_prob(filename):
	f = open(filename, 'r')
	o = pickle.load(f)
	return o


def spreader_test():
	x = np.linspace(-1.,1.)
	y = np.linspace(-1.,1.)
	X,Y = np.meshgrid(x,y)
	
	Z = source_spreader(X,Y,1,1,2,2)

	con = pl.contourf(X,Y,Z)
	pl.colorbar(con)
	
	pl.show()
	
def test_localcoor(z):
	lc = LocalCoor(z)

	print "g   l"
	print "1   ",lc.glo_to_loc(1)
	print "2   ",lc.glo_to_loc(2)
	print "3   ",lc.glo_to_loc(3)
	
	print "l   g"
	print "1   ",lc.loc_to_glo(1)
	print "2   ",lc.loc_to_glo(2)
	print "3   ",lc.loc_to_glo(3)


if __name__ == '__main__':
	test_localcoor(2)
	

