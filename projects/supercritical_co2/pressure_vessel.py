
import math
from CoolProp.CoolProp import PropsSI

f = "CO2"

d = PropsSI("RHOMASS_CRITICAL", f)
M = PropsSI("MOLAR_MASS", f)

print "d",d
print "M",M

T = 273 + 40

P = PropsSI("P", "T", T, "DMASS", d, f)

print "P",P

P_atm = 101300


D = 10E-3
L = 10E-2

V1 = math.pi * D**2/4.0

m = d * V1

R = 8.314

g = 1.3
a = 1.0 / (g - 1.0)

#E = 

V2 = math.pow(P / P_atm * V1**g, 1.0/g)

print "V1 {:16.2e}".format(V1)
print "V2 {:16.2e}".format(V2)

r = math.pow(3.0 * V2 / 4.0 / math.pi, 1.0/3.0)

print "radius",r

V2 = m * R * T / M / P_atm

print "V2 {:16.2e}".format(V2)

r = math.pow(3.0 * V2 / 4.0 / math.pi, 1.0/3.0)

print "radius",r



E = P * V1**g * (V2**(1.0-g) - V1**(1.0-g)) / (1.0-g)

print "E",E

# E = 0.5 * m * v**2
# 2.0 E / m =  v**2

m_proj = 2E-3

v = math.pow(2.0 * E * m_proj, 0.5)

print "speed", v



