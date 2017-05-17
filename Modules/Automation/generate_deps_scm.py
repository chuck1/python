import os
import sys
import argparse

import Case

parser = argparse.ArgumentParser()
parser.add_argument("path_config")
parser.add_argument("path_pyth")
args = parser.parse_args()

def prnt(a):
	print a

with open(args.path_config, 'r') as f:
	case = Case.Case(args.path_config)

dir_python = os.path.join(os.environ["HOME"], "Documents", "Programming", "Python")
dir_auto = os.path.join(dir_python, "Modules", "Automation")

paths = []
paths.append(os.path.join(dir_auto, "Case.py"))
paths.append(os.path.join(dir_auto, "Fluent.py"))
paths.append(args.path_config)
paths.append(args.path_pyth)

sys.stdout.write(";".join(paths))



