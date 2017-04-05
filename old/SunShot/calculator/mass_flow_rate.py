#!/usr/bin/env python

import os
import sys

modules_dir = os.environ["HOME"] + '/Programming/Python/Modules'
sys.path.append(modules_dir)

import Sci.Fluids as Flu

# input
if len(sys.argv) < 7:
	print "usage: ./mass_flow_rate.py <temperature in> <temperature out> <length> <width> <heat flux> <fluid>"
	sys.exit()


T0 = float(sys.argv[1])
T1 = float(sys.argv[2])
l  = float(sys.argv[3])
w  = float(sys.argv[4])
q  = float(sys.argv[5])
f  = sys.argv[6]

def mass_flow_rate( fluid, T0, T1, q ):
	print "hello"

flu = Flu.Fluid(f)

h = flu.enthalpy_change(T0,T1)

rho = flu.get('density', T0)
#mu = flu.get('viscosity',T0)

m = q*l*w/h

l_in = 0.0004

A_in = w*l_in

um = m/rho/A_in

#print "my  = %5s" % mu
print "dh  = %5s" % h
print "rho = %5s" % rho
print "m   = %5s" % m
print "um  = %5s" % um






