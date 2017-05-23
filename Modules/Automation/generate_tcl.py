import sys

import Case

if len(sys.argv) < 4:
	print "usage: {0} <config file> <tcl in file> <tcl file>".format(sys.argv[0])
	sys.exit(1)

path_conf = sys.argv[1]
path_tcl_in = sys.argv[2]
path_tcl = sys.argv[3]

case = Case.Case(path_conf)

lines = case.get_lines_configured(path_tcl_in)



with open(path_tcl, 'w') as f:
	f.writelines(lines)


