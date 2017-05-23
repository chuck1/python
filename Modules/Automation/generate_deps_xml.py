import sys
import argparse

import Case

parser = argparse.ArgumentParser()
parser.add_argument("path_config")
args = parser.parse_args()


def walk(conf):
	#print "<<<<<<<<",conf.path

	for s in conf.sources:
		yield s
	
	for c in conf.config:
		#print ">>>>>>>>",c.path
		yield c.path

		for l in walk(c):
			yield(l)



with open(args.path_config, 'r') as f:
	case = Case.Case(args.path_config)

lst = list(walk(case))

sys.stdout.write(";".join(lst))


