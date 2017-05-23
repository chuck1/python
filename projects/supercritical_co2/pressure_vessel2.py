
import math
from CoolProp.CoolProp import PropsSI

f = "CO2"

d = PropsSI("RHOMASS_CRITICAL", f)
M = PropsSI("MOLAR_MASS", f)

print "d",d
print "M",M

T_dryice = 194

T = 273 + 40

P = PropsSI("P", "T", T, "DMASS", d, f)

print "P",P

P_atm = 101300


D = 10E-3
L = 10E-2

V1 = math.pi * D**2/4.0

m = d * V1

T_t = PropsSI("T_TRIPLE", f)

H1 = PropsSI("H", "T", T_t, "DMASS", d, f)
H2 = PropsSI("H", "T", T, "DMASS", d, f)

print "H", H1
print "H", H2

E1 = H1 * m
E2 = H2 * m

print E2 - E1




n = m / M

print "n",n,"mol"

cp = 183.1 # J/mol K


E = cp * n * (T - T_dryice)

print "E",E





