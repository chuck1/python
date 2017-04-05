#!/usr/bin/env python
import os
import sys
import numpy as np



		
T = float(sys.argv[1])
		
T_inf = 298.0
h_nat = 15.0
sigma = 5.67 * pow(10,-8)
emiss = 0.95

q_abs = 1e6
q_rad = emiss * sigma * (pow(T,4) - pow(T_inf,4))
q_conv = h_nat * (T - T_inf)

eff = q_abs * emiss / (q_abs + q_rad + q_conv)
		
print "eff = {0}".format(eff)




