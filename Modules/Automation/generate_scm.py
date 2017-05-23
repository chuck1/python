import os
import sys
import argparse
import logging

import Case

parser = argparse.ArgumentParser()
parser.add_argument("path_config")
parser.add_argument("path_scm")
args = parser.parse_args()


with open(args.path_config, 'r') as f:
	case = Case.Case(args.path_config)

# boundary conditions

# calculations
# SHOULD BE REPLACED BY PY SCRIPTS IN CONFIG DIRS!!!!

# write

logging.info("writing output to \"{0}\"".format(args.path_scm))

str = case.script_fluent()

with open(args.path_scm, 'w') as f:
	#f.writelines(lines)
	f.write(str)

os.system('dos2unix ' + args.path_scm)



# redo

root, ext = os.path.splitext(args.path_scm)
path = root + '_redo' + ext

str = case.script_fluent_redo()

with open(path, 'w') as f:
	#f.writelines(lines)
	f.write(str)

os.system('dos2unix ' + path)




