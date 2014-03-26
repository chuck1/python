
#import time
#import numpy as np
#import itertools
#from pylab import plot, show, figure, contour
#import pylab as pl
#from mpl_toolkits.mplot3d import Axes3D
#from matplotlib import cm
#from sympy import *
#import math
#import inspect

#spreader_test()

from solver import *

prob = Problem('opt1',
		k = 10.,
		alpha = 1.4,
		alpha_src = 1.4,
		it_max_2 = 20)

x = [0.002,  0.008, 0.005]

y = [0.0015, 0.003, 0.0015, 0.02]

z = [0.008,  0.004, 0.003, 0.002, 0.010, 0.002, 0.003, 0.004, 0.008]

x = np.cumsum(np.append([0],x))
y = np.cumsum(np.append([0],y))
z = np.cumsum(np.append([0],z))

nx = [ 4, 16, 10]
ny = [ 3,  6,  3, 20]
nz = [16,  8,  6,  4,  20, 4,  6,  8, 16]

X = [x,y,z]
N = [nx,ny,nz]

# zi z inner
# zo z outer

# inlet
f_hi_xp   = prob.createPatch( 1, [3,		[0,1,2,3],	[0,1,2,3]],	X, N)

f_hi_yp_1 = prob.createPatch( 2, [[1,2,3],	3,		[0,1,2,3]],	X, N)
f_hi_yp_2 = prob.createPatch( 2, [[0,1],	3,		[0,1]],		X, N)
f_hi_yp_3 = prob.createPatch( 2, [[0,1],	3,		[2,3]],		X, N)

f_hi_ym   = prob.createPatch(-2, [[3,2,1,0],	0,		[3,2,1,0]],	X, N)

f_hi_zo   = prob.createPatch(-3, [[3,2,1,0],	[3,2,1,0],	0],		X, N)

f_hi_zi_1 = prob.createPatch( 3, [[2,3],	[0,1,2,3],	3],		X, N)
f_hi_zi_2 = prob.createPatch( 3, [[0,1,2],	[0,1],		3],		X, N)
f_hi_zi_3 = prob.createPatch( 3, [[0,1,2],	[2,3],		3],		X, N)

stitch(f_hi_xp,   f_hi_yp_1)
stitch(f_hi_xp,   f_hi_ym)
stitch(f_hi_xp,   f_hi_zo)
stitch(f_hi_xp,   f_hi_zi_1)

stitch(f_hi_yp_1, f_hi_yp_2)
stitch(f_hi_yp_1, f_hi_yp_3)
stitch(f_hi_yp_1, f_hi_zo)
stitch(f_hi_yp_1, f_hi_zi_1)
stitch(f_hi_yp_1, f_hi_zi_3)

stitch(f_hi_yp_2, f_hi_zo)

stitch(f_hi_ym,   f_hi_zo)

stitch(f_hi_zi_1, f_hi_zi_2)
stitch(f_hi_zi_1, f_hi_zi_3)

# outlet
f_ho_xp   = prob.createPatch( 1, [3,		[0,1,2,3],	[6,7,8,9]],	X, N)

f_ho_yp_1 = prob.createPatch( 2, [[1,2,3],	3,		[6,7,8,9]],	X, N)
f_ho_yp_2 = prob.createPatch( 2, [[0,1],	3,		[8,9]],		X, N)
f_ho_yp_3 = prob.createPatch( 2, [[0,1],	3,		[6,7]],		X, N)

f_ho_ym   = prob.createPatch(-2, [[3,2,1,0],	0,		[9,8,7,6]],	X, N)

f_ho_zo   = prob.createPatch( 3, [[0,1,2,3],	[0,1,2,3],	9],		X, N)

f_ho_zi_1 = prob.createPatch(-3, [[3,2],	[3,2,1,0],	6],		X, N)
f_ho_zi_2 = prob.createPatch(-3, [[2,1,0],	[1,0],		6],		X, N)
f_ho_zi_3 = prob.createPatch(-3, [[2,1,0],	[3,2],		6],		X, N)

stitch(f_ho_xp,   f_ho_yp_1)
stitch(f_ho_xp,   f_ho_ym)
stitch(f_ho_xp,   f_ho_zo)
stitch(f_ho_xp,   f_ho_zi_1)

stitch(f_ho_yp_1, f_ho_yp_2)
stitch(f_ho_yp_1, f_ho_yp_3)
stitch(f_ho_yp_1, f_ho_zo)
stitch(f_ho_yp_1, f_ho_zi_1)
stitch(f_ho_yp_1, f_ho_zi_3)

stitch(f_ho_yp_2, f_ho_zo)

stitch(f_ho_ym,   f_ho_zo)

stitch(f_ho_zi_1, f_ho_zi_2)
stitch(f_ho_zi_1, f_ho_zi_3)

# channel
f_ch_xp   = prob.createPatch( 1, [2,		[1,2],	[3,4,5,6]],	X, N) # need bc with heated!!!

f_ch_yp   = prob.createPatch( 2, [[0,1,2],	2,	[3,4,5,6]],	X, N)

f_ch_i_ym = prob.createPatch(-2, [[2,1,0],	1,	[4,3]],		X, N) # need bc with heated!!!
f_ch_o_ym = prob.createPatch(-2, [[2,1,0],	1,	[6,5]],		X, N) # need bc with heated!!!

stitch(f_ch_xp, f_hi_zi_1)
stitch(f_ch_xp, f_ho_zi_1)
stitch(f_ch_xp, f_ch_yp)
stitch(f_ch_xp, f_ch_i_ym)
stitch(f_ch_xp, f_ch_o_ym)

# pipe
f_pi_xp = prob.createPatch( 1, [1,	[3,4],	[1,2]],	X, N)

f_pi_zi = prob.createPatch( 3, [[0,1],	[3,4],	2],	X, N)

f_pi_zo = prob.createPatch(-3, [[1,0],	[4,3],	1],	X, N)



f_po_xp = prob.createPatch( 1, [1,	[3,4],	[7,8]],	X, N)

f_po_zi = prob.createPatch(-3, [[1,0],	[4,3],	7],	X, N)

f_po_zo = prob.createPatch( 3, [[0,1],	[3,4],	8],	X, N)




#print faces



prob.solve2(1e-4, 1e-2, True)

"""
#prob.save()


"""
ax = prob.plot3()

lim = 0.05

ax.set_xlim3d(0, lim)
ax.set_ylim3d(0, lim)
ax.set_zlim3d(0, lim)

pl.show()




