#!/usr/bin/env python
import os
import sys
import numpy as np



def efficiency(T, q_abs, T_infr = 298.15, T_infc = 298.15, h_nat = 15.0, emiss = 0.95):
	sigma = 5.67 * pow(10,-8)
	
	q_rad = emiss * sigma * (pow(T,4) - pow(T_infr,4))
	q_conv = h_nat * (T - T_infc)
	
	# thermal
	eff_ther = q_abs / (q_abs + q_rad + q_conv)
	
	# receiver
	eff_recv = eff_ther * emiss
	
	return eff_ther, eff_recv, q_rad, q_conv


if __name__ == "__main__":

        T = 800

        qpp = 4e6

        print(efficiency(T, qpp))







