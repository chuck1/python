import numpy as np
import solver.prob
from solver.patch import stitch

w_total = 6e-2
w_irrad = 2e-2
w_ends = (w_total - w_irrad) / 2.0
pipe = 1.5e-3
w_1 = (w_ends - pipe) / 2.0

l_total = 4e-2
l_irrad = 2e-2
l_1 = (l_total - l_irrad) / 2.0
l_3 = l_irrad - pipe * 2.0

x = [w_1, pipe, w_1, w_irrad, w_1, pipe, w_1]

y = [1e-2, 5e-2]

z = [l_1, pipe, l_3, pipe, l_1]

x = np.cumsum(np.append([0],x))
y = np.cumsum(np.append([0],y))
z = np.cumsum(np.append([0],z))

nx = [10, 10, 10, 50, 10, 10, 10]
ny = [50, 50]
nz = [10, 10, 30, 10, 10]

X = [x,y,z]
n = [nx,ny,nz]

prob = solver.prob.Problem('opt2', X, n, it_max_1 = 1000, it_max_2 = 1000)

prob.create_equation('T', 10.0, 1.5, 1.5)
prob.create_equation('s', 10.0, 1.5, 1.5)

s = 1.0e10

# create patch groups

g_hi_xp		= prob.create_patch_group('hi_xp',	v_0 = {'T':100.0,'s':2.0}, S = {'T':0.0,'s':s})
g_hi_yp		= prob.create_patch_group('hi_yp',	v_0 = {'T':100.0,'s':2.0}, S = {'T':0.0,'s':s})
g_hi_ym		= prob.create_patch_group('hi_ym',	v_0 = {'T':100.0,'s':2.0}, S = {'T':0.0,'s':s})
g_hi_zo		= prob.create_patch_group('hi_zo',	v_0 = {'T':100.0,'s':2.0}, S = {'T':0.0,'s':s})
g_hi_zi		= prob.create_patch_group('hi_zi',	v_0 = {'T':100.0,'s':2.0}, S = {'T':0.0,'s':s})

g_ho_xp		= prob.create_patch_group('ho_xp',	v_0 = {'T':100.0,'s':2.0}, S = {'T':0.0,'s':s})
g_ho_yp		= prob.create_patch_group('ho_yp',	v_0 = {'T':100.0,'s':2.0}, S = {'T':0.0,'s':s})
g_ho_ym		= prob.create_patch_group('ho_ym',	v_0 = {'T':100.0,'s':2.0}, S = {'T':0.0,'s':s})
g_ho_zo		= prob.create_patch_group('ho_zo',	v_0 = {'T':100.0,'s':2.0}, S = {'T':0.0,'s':s})
g_ho_zi		= prob.create_patch_group('ho_zi',	v_0 = {'T':100.0,'s':2.0}, S = {'T':0.0,'s':s})

g_pi		= prob.create_patch_group('pi',		v_0 = {'T':100.0,'s':2.0}, S = {'T':0.0,'s':s})
g_po		= prob.create_patch_group('po',		v_0 = {'T':100.0,'s':2.0}, S = {'T':0.0,'s':s})

g_ch_xp		= prob.create_patch_group('ch_xp',	v_0 = {'T':100.0,'s':2.0}, S = {'T':0.0,'s':s})
g_ch_yp		= prob.create_patch_group('ch_yp',	v_0 = {'T':100.0,'s':2.0}, S = {'T':0.0,'s':s})
g_ch_ym_i	= prob.create_patch_group('ch_ym_i',	v_0 = {'T':100.0,'s':2.0}, S = {'T':0.0,'s':s})
g_ch_ym_o	= prob.create_patch_group('ch_ym_o',	v_0 = {'T':100.0,'s':2.0}, S = {'T':0.0,'s':s})

# create patches
# ym
p_ym_0_0	= g_ym.create_patch('',	-2,[[0,1,2,3],	0,	[0,1]],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
p_ym_0_1	= g_ym.create_patch('',	-2,[[0,1,2,3],	0,	[1,2,3,4]],	v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
p_ym_0_2	= g_ym.create_patch('',	-2,[[0,1,2,3],	0,	[4,5]],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
p_ym_1_0	= g_ym.create_patch('',	-2,[[3,4],	0,	[0,1]],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
p_ym_1_2	= g_ym.create_patch('',	-2,[[3,4],	0,	[4,5]],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
p_ym_2_0	= g_ym.create_patch('',	-2,[[4,5,6,7],	0,	[0,1]],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
p_ym_2_1	= g_ym.create_patch('',	-2,[[4,5,6,7],	0,	[1,2,3,4]],	v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
p_ym_2_2	= g_ym.create_patch('',	-2,[[4,5,6,7],	0,	[4,5]],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})

# yp
p_yp_0_0	= g_yp.create_patch('',	2,[[0,1,2,3],	1,	[0,1]],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})

p_yp_0_1_0	= g_yp.create_patch('',	2,[[0,1],	1,	[1,2,3,4]],	v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
p_yp_0_1_1	= g_yp.create_patch('',	2,[[1,2],	1,	[2,3]],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
p_yp_0_1_2	= g_yp.create_patch('',	2,[[2,3],	1,	[1,2,3,4]],	v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})

p_yp_0_2	= g_yp.create_patch('',	2,[[0,1,2,3],	1,	[4,5]],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
p_yp_1_0	= g_yp.create_patch('',	2,[[3,4],	1,	[0,1]],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
p_yp_1_2	= g_yp.create_patch('',	2,[[3,4],	1,	[4,5]],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
p_yp_2_0	= g_yp.create_patch('',	2,[[4,5,6,7],	1,	[0,1]],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})

p_yp_2_1_0	= g_yp.create_patch('',	2,[[4,5],	1,		[1,2,3,4]],	v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
p_yp_2_1_1	= g_yp.create_patch('',	2,[[5,6],	1,		[2,3]],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
p_yp_2_1_2	= g_yp.create_patch('',	2,[[6,7],	1,		[1,2,3,4]],	v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})

p_yp_2_2	= g_yp.create_patch('',	2,[[4,5,6,7],	1,		[4,5]],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})

# xp
p_xm		= g_xp.create_patch('p_xp', -1,	[0,	[0,1],		[0,1,2,3,4,5]],	v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
p_xp		= g_xp.create_patch('p_xp', 1,	[7,	[0,1],		[0,1,2,3,4,5]],	v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})

p_zm		= g_zm.create_patch('p_zm', -3,	[[3,2,1,0],	[3,2,1,0],	0],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})


# inlet
p_hi_xp   = g_hi_xp.create_patch('p_hi_xp',	1, [3,		[0,1,2,3],	[0,1,2,3]],	v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})

p_hi_yp_1 = g_hi_yp.create_patch('p_hi_yp_1',	2, [[1,2,3],	3,		[0,1,2,3]],	v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
p_hi_yp_o = g_hi_yp.create_patch('p_hi_yp_o',	2, [[0,1],	3,		[0,1]],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
p_hi_yp_i = g_hi_yp.create_patch('p_hi_yp_i',	2, [[0,1],	3,		[2,3]],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})

p_hi_ym   = g_hi_ym.create_patch('p_hi_ym',	-2,[[3,2,1,0],	0,		[3,2,1,0]],	v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})

p_hi_zo   = g_hi_zo.create_patch('p_hi_zo',	-3,[[3,2,1,0],	[3,2,1,0],	0],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})

p_hi_zi_1 = g_hi_zi.create_patch('p_hi_zi_1',	3, [[2,3],	[0,1,2,3],	3],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
p_hi_zi_2 = g_hi_zi.create_patch('p_hi_zi_2',	3, [[0,1,2],	[0,1],		3],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
p_hi_zi_3 = g_hi_zi.create_patch('p_hi_zi_3',	3, [[0,1,2],	[2,3],		3],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})

# outlet
p_ho_xp   = g_ho_xp.create_patch('p_ho_xp',	1, [3,		[0,1,2,3],	[6,7,8,9]],	v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})

p_ho_yp_1 = g_ho_yp.create_patch('p_ho_yp_1',	2, [[1,2,3],	3,		[6,7,8,9]],	v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
p_ho_yp_o = g_ho_yp.create_patch('p_ho_yp_o',	2, [[0,1],	3,		[8,9]],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
p_ho_yp_i = g_ho_yp.create_patch('p_ho_yp_i',	2, [[0,1],	3,		[6,7]],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})

p_ho_ym   = g_ho_ym.create_patch('p_ho_ym',-2, [[3,2,1,0],	0,		[9,8,7,6]],	v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})

p_ho_zo   = g_ho_zo.create_patch('p_ho_zo', 3, [[0,1,2,3],	[0,1,2,3],	9],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})

p_ho_zi_1 = g_ho_zi.create_patch('p_ho_zi_1',-3, [[3,2],	[3,2,1,0],	6],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
p_ho_zi_2 = g_ho_zi.create_patch('p_ho_zi_2',-3, [[2,1,0],	[1,0],		6],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
p_ho_zi_3 = g_ho_zi.create_patch('p_ho_zi_3',-3, [[2,1,0],	[3,2],		6],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})

# channel
# need bc with heated!!!
p_ch_xp   = g_ch_xp.create_patch('p_ch_xp',	1, [2,		[1,2],	[3,4,5,6]],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
p_ch_yp   = g_ch_yp.create_patch('p_ch_yp',	2, [[0,1,2],	2,	[3,4,5,6]],		v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
p_ch_i_ym = g_ch_ym_i.create_patch('p_ch_i_ym',-2, [[2,1,0],	1,	[4,3]],			v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
p_ch_o_ym = g_ch_ym_i.create_patch('p_ch_o_ym',-2, [[2,1,0],	1,	[6,5]],			v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})


# pipe
p_pi_xp = g_pi.create_patch('p_pi_xp', 1, [1,		[3,4],	[1,2]],				v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
p_pi_zi = g_pi.create_patch('p_pi_zi', 3, [[0,1],	[3,4],	2],				v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
p_pi_zo = g_pi.create_patch('p_pi_zo',-3, [[1,0],	[4,3],	1],				v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})

p_po_xp = g_po.create_patch('p_po_xp', 1, [1,		[3,4],	[7,8]],				v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
p_po_zi = g_po.create_patch('p_po_zi',-3, [[1,0],	[4,3],	7],				v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})
p_po_zo = g_po.create_patch('p_po_zo', 3, [[0,1],	[3,4],	8],				v_bou = {'T':[[0.0,0.0],[0.0,0.0]],'s':[[1.0,1.0],[1.0,1.0]]})

# stitching
# inlet
stitch(p_hi_xp,   p_hi_yp_1)
stitch(p_hi_xp,   p_hi_ym)
stitch(p_hi_xp,   p_hi_zo)
stitch(p_hi_xp,   p_hi_zi_1)

stitch(p_hi_yp_1, p_hi_yp_o)
stitch(p_hi_yp_1, p_hi_yp_i)
stitch(p_hi_yp_1, p_hi_zo)
stitch(p_hi_yp_1, p_hi_zi_1)
stitch(p_hi_yp_1, p_hi_zi_3)

stitch(p_hi_yp_o, p_hi_zo)

stitch(p_hi_ym,   p_hi_zo)

stitch(p_hi_zi_1, p_hi_zi_2)
stitch(p_hi_zi_1, p_hi_zi_3)

# outlet
stitch(p_ho_xp,   p_ho_yp_1)
stitch(p_ho_xp,   p_ho_ym)
stitch(p_ho_xp,   p_ho_zo)
stitch(p_ho_xp,   p_ho_zi_1)

stitch(p_ho_yp_1, p_ho_yp_o)
stitch(p_ho_yp_1, p_ho_yp_i)
stitch(p_ho_yp_1, p_ho_zo)
stitch(p_ho_yp_1, p_ho_zi_1)
stitch(p_ho_yp_1, p_ho_zi_3)

stitch(p_ho_yp_o, p_ho_zo)

stitch(p_ho_ym,   p_ho_zo)

stitch(p_ho_zi_1, p_ho_zi_2)
stitch(p_ho_zi_1, p_ho_zi_3)

# channel
stitch(p_ch_xp, p_hi_zi_1)
stitch(p_ch_xp, p_ho_zi_1)
stitch(p_ch_xp, p_ch_yp)
stitch(p_ch_xp, p_ch_i_ym)
stitch(p_ch_xp, p_ch_o_ym)

stitch(p_ch_yp, p_hi_zi_3)
stitch(p_ch_yp, p_ho_zi_3)

stitch(p_ch_i_ym, p_hi_zi_2)
stitch(p_ch_o_ym, p_ho_zi_2)

# pipe
# -inlet
stitch(p_pi_xp, p_hi_yp_1)

stitch(p_pi_zo, p_hi_yp_o)
stitch(p_pi_zi, p_hi_yp_i)

# -outlet
stitch(p_po_xp, p_ho_yp_1)

stitch(p_po_zo, p_ho_yp_o)
stitch(p_po_zi, p_ho_yp_i)


def solve_with_source():
	prob.solve2(1e-4, 1e-2, True)
	prob.solve('s', 1e-2, True)
	prob.value_add('s', -1.0)
	prob.value_normalize('s')
	prob.copy_value_to_source('s','T')
	prob.solve2('T', 1e-2, 1e-2, True)


prob.solve('T', 1e-2, True)

#prob.save()

#prob.plot('T')

prob.write('T')


