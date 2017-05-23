import struct
import numpy as np
import matplotlib.pyplot as plt
import sys
import getopt
import collections

retopt = collections.namedtuple('retopt', ['x', 'y', 'style'])

def usage():
	print "x- <file> specify x data file"
	print "y- <file> specify y data file"
	print "-loglog use base 10 log scale on x and y axes"
	

def main(argv):                         
	
	try:                                
		opts, args = getopt.getopt(argv, "hx:y:l", ["help","x","y","loglog"])
	except getopt.GetoptError:           
		usage()                          
		sys.exit(2)
	
	xfile = "";
	yfile = "";
	style = "";
	
	for opt, arg in opts:                
		if opt in ("-h", "--help"):      
			usage()
			sys.exit()
		elif opt in ("-x"): 
			xfile = arg
		elif opt in ("-y"):
			yfile = arg
		elif opt in ("-l","-loglog"):
			style = "loglog"

	ro = retopt(xfile,yfile,style);
	return ro


if __name__ == "__main__":
	ro = main(sys.argv[1:])



with open(ro.x, "rb") as f:
	x = np.fromfile(f, float)

with open(ro.y, "rb") as f:
	y = np.fromfile(f, float)


#print x
#print y

if ro.style in ("loglog"):
	plt.loglog(x, y)
else:
	plt.plot(x, y)

plt.draw()
