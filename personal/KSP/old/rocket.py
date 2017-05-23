import math
import matplotlib.pyplot as plt
import os
import sys
import numpy as np
import itertools

class part:
	def __init__(self, name, m):
		self.m = m
		self.name = name
	
class engine:
	def __init__(self, name, m, isp_atm, isp_vac, thrust):
		self.name = name
		self.m = m
		self.isp_atm = isp_atm
		self.isp_vac = isp_vac
		self.thrust = thrust
	def get_isp_vac(self):
		return self.isp_vac
	def get_isp_atm(self):
		return self.isp_atm

	def get_thrust(self):
		return self.thrust
	
class tank:
	def __init__(self, name, m, m_dry):
		self.name = name
		self.m = m
		self.m_dry = m_dry
	def get_m_dry(self):
		return self.m_dry




liquidEngine1       = engine("LV-T30 Liquid Fuel Engine", 1.25, 320.0, 370.0, 215.0)
liquidEngine2       = engine("LV-T45 Liquid Fuel Engine", 1.50, 320.0, 370.0, 200.0)
liquidEngine3       = engine("LV-909 Liquid Fuel Engine", 0.5,  300.0, 390.0,  50.0)
engineLargePoodle   = engine("Rockomax \"Poodle\" Liquid Engine",   2.5,  270.0, 390.0, 220.0)
engineLargeSkipper  = engine("Rockomax \"Skipper\" Liquid Engine",  4.0,  300.0, 350.0, 650.0)
engineLargeMainsail = engine("Rockomax \"Mainsail\" Liquid Engine", 6.0,  280.0, 330.0,1500.0)
nuclearEngine       = engine("LV-N Atomic Rocket Motor",            2.25, 220.0, 800.0,  60.0)
toroidalAerospike   = engine("Toroidal Aerospike Rocket",           1.5,  388.0, 390.0, 175.0)


fuelTankSmall      = tank("FL-T200 Fuel Tank",            1.125, 0.125)
fuelTank           = tank("FL-T400 Fuel Tank",            2.25,  0.25)
fuelTank_Long      = tank("FL-T800 Fuel Tank",            4.5,   0.5)
fuelTank4_2        = tank("Rockomax X200-8 Fuel Tank",    4.5,   0.5)
fuelTank2_2        = tank("Rockomax X200-16 Fuel Tank",   9.0,   1.0)
fuelTank1_2        = tank("Rockomax X200-32 Fuel Tank",  18.0,   2.0)
fuelTank3_2        = tank("Rockomax Jumbo-64 Fuel Tank", 36.0,   4.0)


largeCrewedLab     = part("Mobile Processing Lab MPL-LG-2", 3.5)
mk1pod             = part("Command Pod Mk1",                0.8)
mk1_2pod           = part("Command Pod Mk1-2",              4.0)
landerCabinSmall   = part("Mk1 Lander Can",                 0.66)
landerCabinLarge   = part("Mk2 Lander Can",                 2.66)

RCSTank1_2         = part("FL_R1 RCS Fuel Tank",            3.4)




class Stage:
	def __init__(self):
		self.parts   = []
		self.tanks   = []
		self.engines = []

	def get_mass_total(self):
		m = 0.0
		for p in self.parts:
			m += p[0] * p[1].m
		for p in self.tanks:
			m += p[0] * p[1].m
		for p in self.engines:
			m += p[0] * p[1].m
		return m
	def get_mass_dry(self):
		m = 0.0
		for p in self.parts:
			m += p[0] * p[1].m
		for p in self.tanks:
			m += p[0] * p[1].m_dry
		for p in self.engines:
			m += p[0] * p[1].m

		return m
	def get_isp_vac(self):
		n = 0.0
		d = 0.0
		for p in self.engines:
			n += p[1].get_thrust() * p[0]
			d += p[1].get_thrust() / p[1].get_isp_vac() * p[0]
		if d > 0:
			return n / d
		else:
			return 0.0
	def get_isp_atm(self):
		n = 0.0
		d = 0.0
		for p in self.engines:
			n += p[1].get_thrust() * p[0]
			d += p[1].get_thrust() / p[1].get_isp_atm() * float(p[0])
		if d > 0:
			return n / d
		else:
			return 0.0
	def get_thrust(self):
		t = 0.0
		for p in self.engines:
			t += p[1].get_thrust() * p[0]
		return t

	
class Rocket:
	def __init__(self):
		self.stages = []
	
	def add(self, s, q):
		for a in range(q):
			self.stages.append(s)

	def deltav(self):
		dv = []
		m = self.get_m_total_list()
		
		for s in self.stages:
			m.pop(0)
			m_t = sum(m) + s.get_mass_total()
			m_d = sum(m) + s.get_mass_dry()
			isp = s.get_isp_vac() * 9.81
			#print "m_t",m_t
			#print "m_d",m_d
			#print "isp",isp
			if m_d == 0.0:
				dv.append(0.0)
			else:
				dv.append( isp * math.log(m_t / m_d) )
		#print dv
		return dv

	def get_m_total_list(self):
		m = []
		for s in self.stages:
			m.append(s.get_mass_total())
		return m
	def get_m_total(self):
		return sum(self.get_m_total_list())
	def get_m_dry_list(self):
		m = []
		for s in self.stages:
			m.append(s.get_m_dry())
		return m
	def get_m_dry(self):
		return sum(self.get_m_dry_list())
	
	def get_m_ratio(self):
		m_t = self.get_m_total()
		m_d = self.get_m_dry()
		m_f = m_t - m_d
		return m_f / m_t



# If the program is run directly or passed as an argument to the python
# interpreter then create a HelloWorld instance and show it
if __name__ == "__main__":
    r = Rocket()    

    s = Stage()

    s.parts.append((1,mk1pod))
    s.tanks.append((1,fuelTank4_2))
    s.engines.append((1,engineLargeMainsail))

    r.add(s,1)

    print r.deltav()






