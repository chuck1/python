#!/usr/bin/env python

import sys
import os
import numpy as np
import csv
import matplotlib.pyplot as plt

module_dir = os.environ["HOME"] + "/Programming/Python/Modules/"
sys.path.append(module_dir)

def empty_string(s):
	if s == '':
		return False
	
	return True

def read(filename, delim=','):
	filename_npy = filename + ".npy"
	
	try:
		data = np.load(filename_npy)
		print "reading binary"
	except IOError:
		print "reading text"
		
		try:
			f = open( filename, 'rb' )

			reader = csv.reader( f, delimiter=delim, quoting=csv.QUOTE_NONNUMERIC, skipinitialspace=True )
			
			# skip first line
			
			
			rows=[]
	
			r = 0
			while 1:
				row = []
				
				try:
					row = reader.next()
	
					#print row
	
					row = filter(empty_string, row)
	
					#print row
	
							#print row
					
					
					r += 1
				except ValueError:
					#print "ValueError"
					continue
				except NameError as err:
					print err
					sys.exit(0)
				except:
					#print row
					print sys.exc_info()[0]
					break
				
				rows.append( row )
			
			data = np.array( rows )
			
			np.save(filename,data)
			
		except IOError as err:
			print err
			sys.exit(0)
	
	return data
	
	
