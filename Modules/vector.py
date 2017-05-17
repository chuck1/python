import numpy as np
import math

def magn(a):
	return math.sqrt( np.sum( a * a ) )

def norm(a):
	return a / magn(a)

