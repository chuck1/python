import os
import sys
import argparse

import Case

parser = argparse.ArgumentParser()
parser.add_argument("path_config")
parser.add_argument("path_tcl_in")

args = parser.parse_args()

with open(args.path_config, 'r') as f:
	case = Case.Case(args.path_config)

# todo march through tcl sources to find all deps

files = [args.path_config, args.path_tcl_in]

sys.stdout.write(";".join(files))


