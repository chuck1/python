import sys
import math
import numpy as np
import pylab as pl
#from units import unit
#import units.predefined
import pydoc

#units.predefined.define_units()

#import Sci.Fluid.pressure as pres
#import Sci.Fluid.heat as heat

import Sci.Fluids as fl
import Sci.Solve.shooting as shoot

import Sci.Zone


def plot(y,y_str):
	fig = pl.figure()
	ax = fig.add_subplot(111)
	ax.plot(x,y)
	ax.set_xlabel(x_str)
	ax.set_ylabel(y_str)

def plot2(z,z_str):
	fig = pl.figure()
	ax = fig.add_subplot(111)
	con = ax.contourf(x,y,z)
	cbar = pl.colorbar(con)
	cbar.ax.set_ylabel(z_str)
	ax.set_xlabel(x_str)
	ax.set_ylabel(y_str)
	
def pressure_drop_from_diameter(z, D):
	z.D = D
	z.run()
	return z.dp

def pressure_drop_from_square_channel(z, D):
	z.W_chan = D
	z.H_chan = D
	z.W_wall = D
	z.run()
	return z.dp

# ========================================================================


rz = Sci.Zone.RectZone(
		1e-2,
		1e-2,
		4e6,
		'ms1',
		300 + 273.15,
		600 + 273.15)

rz.fluid_operating_pressure = 10 * 1e5

# stress in pin

#known

print
print "staggered"
print

ch = Sci.Zone.Staggered()
ch.copy(rz)

ch.D = np.array(5e-4)
#ch.D = 4e-4 + np.arange(0.0,1.0,0.01) * 5e-4

ch.PT = 2.0
#ch.PT = np.arange(2.0, 5.0, 1.0)

# choose independent var

#ch.D, ch.PT = np.meshgrid(ch.D, ch.PT)

y = ch.PT
y_str = 'PT'

x = ch.D/1e-6
x_str = 'D micrometer'

# calc

#plot2(stress_max/1e6, 'stress')
#plot2(ch.dp/1e5, 'dp bar')
#pl.show()

# find diameter that gives desired pressure drop
#D = shoot.shooting(ch, [2e-4, 6e-4], pressure_drop_from_diameter, 0.6e5 * np.ones(np.shape(ch.PT)))
D = 250e-6

ch.run()

ch.disp()

#Nu = heat.cross_flow_tube_bank_staggered(ch.Re, ch.Pr)

print
#print "rectangular"
print

ch2 = Sci.Zone.Rectangular()
ch2.W_chan = 0.000055
ch2.H_chan = 0.000055
ch2.W_wall = 0.000055

ch2.copy(rz)

# find diameter that gives desired pressure drop
D = shoot.shooting(ch2, [1e-6, 1e-4], pressure_drop_from_square_channel, 1e5)

ch2.run()

#ch2.disp()





