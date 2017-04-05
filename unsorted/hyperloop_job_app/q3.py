import numpy as np
import pylab as pl

def black_body_Q(T):
    return 5.67 * 10**(-8) * T**4


# differential ring element to opposed ring element on coaxial disk
# dF/dR =
def vf_1(r1, r2, h):
    R = r2/r1
    H = h/r1
    Y = np.power(H,2) + np.power(R,2) + 1
    return (2. * R * np.power(H,2) * Y) / ((np.power(Y,2) - 4. * np.power(R,2))**(1.5))

def vf_2(r1, r2_a, r2_b, h):
    #print "vf_2"
    
    n = 2000
    dr2 = (r2_b - r2_a) / n
    R2 = r2_a + (np.arange(n) + 0.5) * dr2
    
    #print R2

    P = vf_1(r1, R2, h)

    dR_dr2 = 1 / r1

    dR = dR_dr2 * dr2

    #print P
    #print dR

    #print P*dR

    return np.sum(P*dR)

def vf_3(r1_a, r1_b, r2_a, r2_b, h):
    print "vf_3"

    n = 2000
    dr1 = (r1_b - r1_a) / n
    R1 = r1_a + (np.arange(n) + 0.5) * dr1
    
    vfunc = np.vectorize(vf_2)
    
    dvf = vfunc(R1, r2_a, r2_b, h)
    
    return np.sum(dvf * dr1)
    
r1 = 1.
r2 = 1.
h  = 1.

n = 10

dr1 = r1 / n
R1 = (np.arange(n)+0.5) * dr1

dr2 = r2 / n
R2 = (np.arange(n)+0.5) * dr2

#print R1
#print dr1

#print R2
#print dr2

# for constant r2
#print vf_1(R1, r2, h)

dR_dr1 = -r2 / R1**2

#print dR_dr1



# for constant r1
#print vf_1(r1, R2, h)

dR_dr2 = 1 / r1

#print dR_dr2



#vf_2(r1, 0, r2, h)

r1 = 1. / np.logspace(-1,1,10)

print r1

#vf_2(1., 0., 1., h)

def test():
    vfunc = np.vectorize(vf_3)

    z = vfunc(0., r1, 0., 1., 1.)
    
    pl.plot(h/r1,z)
    pl.xscale('log')
    pl.show()

print vf_3(0., 1., 0., 1., 1.)


