import math

def cone_surface_area(r, h):
    return math.pi * r * math.sqrt(h**2 + r**2)

def cone_trunc_surface_area(r1, r2, h):
    h1 = h * r1 / (r1 - r2)
    h2 = h1 - h
    
    A1 = cone_surface_area(r1, h1)
    A2 = cone_surface_area(r2, h2)
    
    return A1 - A2
    
# coaxial disks

def vf_1(r1, r2, L):
    R1 = r1/L
    R2 = r2/L
    S = 1 + (1 + R2**2) / R1**2
    F = 0.5 * (S - (S**2 - 4*(r2/r1)**2)**(0.5))
    return F


r1 = 0.5
r3 = 0.25
L  = 0.5

A1 = math.pi * r1**2
A3 = math.pi * r3**2
A2 = cone_trunc_surface_area(r1, r3, L)

F31 = vf_1(r3,r1,L)

F32 = 1 - F31

F23 = F32

F13 = vf_1(r1,r3,L)

F12 = 1 - F13

F21 = F12 * A1 / A2

F23 = F32 * A3 / A2

F22 = 1 - F21 - F23

s = 5.67 * 10**-8

T1 = 200 + 273.15
T2 = 200 + 273.15
T3 =  20 + 273.15

Eb1 = s * T1**4
Eb2 = s * T2**4
Eb3 = s * T3**4

Q13 = Eb1 * A1 * F13 - Eb3 * A3 * F31
Q23 = Eb2 * A2 * F23 - Eb3 * A3 * F32


print "A1 ",A1
print "A2 ",A2
print "A3 ",A3
print
print "F13",F13
print "F12",F12
print
print "F21",F21
print "F22",F22
print "F23",F23
print
print "F31",F31
print "F32",F32
print
print "Q13",Q13
print "Q23",Q23
print "Q  ",Q13+Q23








