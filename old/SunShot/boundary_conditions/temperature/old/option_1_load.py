from solver import *

prob = load_prob('case_opt1')

prob.plot3()
ax = prob.plot3()

lim = 0.05

ax.set_xlim3d(0, lim)
ax.set_ylim3d(0, lim)
ax.set_zlim3d(0, lim)

pl.show()


