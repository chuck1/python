#!/usr/bin/env python

import sys, os
import numpy as np
import math
import scipy.optimize

module_dir = os.environ["HOME"] + "/Documents/Programming/Python/Modules/"
sys.path.append(module_dir)

import csv

import argparse

from funcs import *

def convert_arg_line_to_args(self, arg_line):
	for arg in arg_line.split():
		if not arg.strip():
			continue
		yield arg

class Action(argparse.Action):
	def __call__(self, parser, namespace, values, option_string=None):
		if not getattr(namespace, 's'):
			parser.error("requires -s")
		else:
			setattr(namespace,self.dest,values)


if __name__=='__main__':
	
	parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
	parser.add_argument('-p', action="store_true")
	parser.add_argument('-s', type=float, help='half-width of heated surface')
	parser.add_argument('-f', type=float, help='average flux for profile file')
	parser.add_argument('--prof', action=Action, help='write profile file')
	parser.add_argument('-x', type=float, help='x origin for profile file')
	parser.add_argument('-y', type=float, help='y origin for profile file')
	parser.add_argument('-z', type=float, help='z origin for profile file')
	parser.add_argument('filename', help='csv file')
	args = parser.parse_args()
	
	
	data = get_csv_data(args.filename)

	# extract x and y
	x = data[:,0]
	y = data[:,1]
	
	# correct units
	x = x * 1e-3
	y = y * 1e4
	
	x_sort = np.sort(x)

	p,_ = scipy.optimize.leastsq(errfun2, [1.0e6, -1.0e3, 0.0], args=(x, y))
	

	print "{0:16}{1}".format("p", p)

	
	


	if args.f and args.s:

		print "{0:16}{1: e}".format("flux", args.f)
		
		f_int_1 = numerically_integrate_2D(p, fun3xy, [0.0, args.s], [0.0, args.s])
		
		p2 = np.array(p)
		p2[0] = p2[0] * args.f / f_int_1
		
		print "{0:16}{1}".format("p scaled", p)
		
		f_int_2 = numerically_integrate_2D(p, fun3xy, [0.0, args.s], [0.0, args.s])
		
	
	if args.p:
		import pylab as pl

		leg = []
		
		pl.plot(x,y,'o')
		leg.append('experimental')
		
		pl.plot(x_sort,fun2(p,x_sort))
		leg.append('normal dist')
	
		if args.f and args.s:
                        pl.plot(x_sort,fun2(p2,x_sort))
			leg.append('normal dist scaled')
		

		pl.xlabel('position (m)')
		pl.ylabel('heat flux (W/m2)')
		pl.legend(leg, loc='lower center')
		pl.show()
	
		

	if args.prof:
		import fluent
		
		xe = np.array([0, args.s * 2.0])
		xe += args.x
		
		ze = np.array([0, args.s * 2.0])
		ze += args.z

		xm = np.mean(xe)
		zm = np.mean(ze)

		print "{0:16}{1}".format("xe", xe)
		print "{0:16}{1}".format("ze", ze)
		print "{0:16}{1}".format("xm", xm)
		print "{0:16}{1}".format("zm", zm)
	
		X,Z,F = fun_grid(p2, fun3xy, xe, ze, 20, xm, zm)
	
		Y = np.zeros(np.shape(X)) + args.y

		if args.p:
			con = pl.contourf(X,Z,F)
			pl.colorbar(con)
			pl.show()
		
		prof = fluent.profile.Profile(
				args.prof,
				'solar',
				['x','y','z','flux'],
				np.array([X,Y,Z,F]))

		print "write profile with {0} points".format(np.size(X))

		prof.write()





	
