
import numpy as np

import scipy.optimize

def T2_poly(T1,P1,P2):

    num = P1**(1-n) * T1**n

    den = P2**(1-n)

    T2 = (num/den)**(1/n)

    return T2

# assume air
cp = 1000
n = 1.4

# stated in prob
T1 = 293
P1  = 1
mdot = 7

r_c1 = 4
r_c2 = 3

r_t1 = 3.75
r_t2 = 3.2


T6 = 1500
T8 = 1450

# solve

P10 = 1

P2 = r_c1 * P1
P3 = P2
P4 = r_c2 * P3


P5 = P4
P6 = P5
P7 = P6 / r_t1
P8 = P7
P9 = P8 / r_t2

T3 = T1

T2 = T2_poly(T1,P1,P2)
T4 = T2_poly(T3,P3,P4)
T7 = T2_poly(T6,P6,P7)
T9 = T2_poly(T8,P8,P9)

T5  = T9
T10 = T4



W_c1 = mdot * cp * (T2 - T1)
W_c2 = mdot * cp * (T4 - T3)
W_t1 = mdot * cp * (T6 - T7)
W_t2 = mdot * cp * (T8 - T9)
    
P = W_t1 + W_t2 - W_c1 - W_c2

bwr = (W_c1 + W_c2)/(W_t1 + W_t2)

Q1 = cp * mdot * (T6 - T5)
Q2 = cp * mdot * (T8 - T7)

eff = P / (Q1+Q2)

print "T1 ",T1
print "T2 ",T2
print "T3 ",T3
print "T4 ",T4
print "T5 ",T5
print "T6 ",T6
print "T7 ",T7
print "T8 ",T8
print "T9 ",T9
print "T10",T10
print
print "P1 ",P1
print "P2 ",P2
print "P3 ",P3
print "P4 ",P4
print "P5 ",P5
print "P6 ",P6
print "P7 ",P7
print "P8 ",P8
print "P9 ",P9
print "P10",P10
print
print "W_c1",W_c1
print "W_c2",W_c2
print "W_t1",W_t1
print "W_t2",W_t2
print "P   ",P
print "bwr ",bwr
print
print "Q1  ",Q1
print "Q2  ",Q2

print "eff ",eff

