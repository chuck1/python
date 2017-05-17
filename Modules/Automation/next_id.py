import os
import re
import argparse

import Automation


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('dir')
	args = parser.parse_args()
	
	print Automation.next_id(args.dir)

