
from CoolProp.CoolProp import PropsSI

f = "co2"


T_c = PropsSI("T_CRITICAL", f)
P_c = PropsSI("P_CRITICAL", f)

D_c = PropsSI("RHOMASS_CRITICAL", f)

T_t = PropsSI("T_TRIPLE", f)
P_t = PropsSI("P_TRIPLE", f)

print "reference"
print "tempreature of liquid nitrogen:       77.4"
print "temperature of solid carbon dioxide: 194.7"
print

print "critical point"
print "T",T_c
print "P",P_c
print "D",D_c

print "triple point"
print "T", T_t
print "P", P_t

P_atm = 101300


if P_t < P_atm:
    D = PropsSI("DMASS", "P", P_atm, "Q", 0, f)
    print "must cool to", PropsSI("T", "P", P_atm, "Q", 0, f)
    print "D:",D


