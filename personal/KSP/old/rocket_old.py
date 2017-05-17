import math
import matplotlib.pyplot as plt

class part:
	def __init__(self, name, m):
		self.m = m
	def get_m_dry(self):
		return self.m
	def get_Isp(self):
		return 0.0
	def get_thrust(self):
		return 0.0
	
class engine(part):
	def __init__(self, name, m, Isp_atm, Isp_vac, thrust):
		self.m = m
		self.Isp_atm = Isp_atm
		self.Isp_vac = Isp_vac
		self.thrust = thrust
	def get_Isp(self):
		return self.Isp_vac
	def get_thrust(self):
		return self.thrust
	
class fuel_tank(part):
	def __init__(self, name, m, m_dry):
		self.m = m
		self.m_dry = m_dry
	def get_m_dry(self):
		return self.m_dry

class stage:
	def __init__(self):
		self.parts = []
	
	def add(self, p, quantity):
		self.parts.append((p,quantity))
	
	def m_total(self):
		m = 0.0
		for p,q in self.parts:
			m += p.m * float(q)
		return m
	def get_m_dry(self):
		m = 0.0
		for p,q in self.parts:
			m += p.get_m_dry() * float(q)
		return m
	def isp(self):
		n = 0.0
		d = 0.0
		for p,q in self.parts:
			if isinstance(p, engine):
				n += p.get_thrust() * float(q)
				d += p.get_thrust() / p.get_Isp() * float(q)
		
		return n / d
	def get_thrust(self):
		t = 0
		for p,q in self.parts:
			if isinstance(p, engine):
				t += p.get_thrust() * float(q)
		return t
		

class rocket:
	
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
			m_t = sum(m) + s.m_total()
			m_d = sum(m) + s.get_m_dry()
			isp = s.isp() * 9.81
			#print "m_t",m_t
			#print "m_d",m_d
			#print "isp",isp
			
			dv.append( isp * math.log(m_t / m_d) )
		print dv
		return sum(dv)

	def get_m_total_list(self):
		m = []
		for s in self.stages:
			m.append(s.m_total())
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
	def get_TWR(self, g):
		twr = []
		m = self.get_m_total_list()
		
		for s in self.stages:
			twr.append(s.get_thrust() / sum(m) / g)
			m.pop(0)
		return twr
	



s0 = stage()
s0.add(engineLargeSkipper, 1)
s0.add(fuelTank3_2, 3)


s1 = stage()
s1.add(fuelTank4_2, 1)
s1.add(fuelTankSmall, 4)
s1.add(liquidEngine3, 4)

s2 = stage()
s2.add(landerCabinLarge, 1)
s2.add(fuelTank4_2, 2)
s2.add(fuelTank2, 8)
#s2.add(engineLargeMainsail, 4)
s2.add(liquidEngine3, 8)


r = rocket()
#r.add(s0,1)
#r.add(s1,1)
r.add(s2,1)

print "TWR",r.get_TWR(7.85)

print r.deltav()
#print r.get_m_ratio()


