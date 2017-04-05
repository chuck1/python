#!/usr/bin/env python

import re
import os
import sys
import math
import numpy as np
import lxml.etree as etree
import logging
import matplotlib.pyplot as plt

modules_dir = os.environ["HOME"] + "/Programming/Python/Modules"
sys.path.append( modules_dir )

import Sci.Fluids as flu
import plot
import Sci.Geo as Geo
import XML


if len(sys.argv) < 4:
	print "usage: {0} FLUID PROPERTY TEMPERATURE".format(sys.argv[0])
	sys.exit(0)

string_fluid = sys.argv[1]
string_property = sys.argv[2]
temperature = float(sys.argv[3])

f = flu.Fluid(string_fluid)

print f.get(string_property, temperature)



